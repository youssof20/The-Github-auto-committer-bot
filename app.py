import base64
import json
import os
import logging
import datetime
import threading
from cryptography.fernet import Fernet
from flask import Flask, request, render_template
import requests
import mysql.connector
import schedule
import time
import configs

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize encryption
crypt = Fernet(os.environ.get("FERNET_KEY"))

# Constants
FULL_REPO_NAME_POST_CREATION = "Hello, all Lazy People"


@app.route("/", methods=["GET"])
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/register-user", methods=["POST"])
def register_user():
    """Register a new user and create a private repository."""
    user_token = request.form.get("token")
    encrypted_token = crypt.encrypt(user_token.encode())

    # Create a new private repository
    repo_body = {
        "name": configs.HARDCODED_REPOSITORY_NAME,
        "description": "Just fooling along for fun - No harm intended",
        "private": True,
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    repo_url = f"{configs.GITHUB_API_URL}/user/repos"

    logger.info(f"Sending POST request to {repo_url}")
    response = requests.post(repo_url, headers=headers, json=repo_body)

    if response.status_code != 201:
        logger.error(f"Failed to create repository: {response.json()}")
        return render_template("error_page.html")

    logger.info("Repository created successfully")
    owner_name = response.json().get("owner").get("login")

    # Store user details in the database
    try:
        db_connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=os.environ.get("MYSQL_PORT"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        if db_connection.is_connected():
            logger.info("Connected to MySQL Database")
            cursor = db_connection.cursor()
            insert_query = """
                INSERT INTO all_registered_users 
                (username, date_created, to_end_date, token, is_active, file_sha) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    owner_name,
                    datetime.datetime.today(),
                    datetime.datetime.today() + datetime.timedelta(days=7),
                    encrypted_token.decode("utf-8"),
                    1,
                    "",
                ),
            )
            db_connection.commit()
            cursor.close()
            db_connection.close()
        else:
            logger.error("Failed to connect to MySQL Database")
            return render_template("error_page.html")
    except Exception as e:
        logger.error(f"Database error: {e}")
        return render_template("error_page.html")

    # Create README file in the repository
    readme_response = create_readme_file(owner_name, user_token)
    if readme_response.status_code != 201:
        logger.error(f"Failed to create README file: {readme_response.json()}")
        return render_template("error_page.html")

    # Update file SHA in the database
    file_sha = readme_response.json().get("content").get("sha")
    try:
        db_connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=os.environ.get("MYSQL_PORT"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        if db_connection.is_connected():
            logger.info("Connected to MySQL Database")
            cursor = db_connection.cursor()
            update_query = """
                UPDATE all_registered_users 
                SET file_sha = %s 
                WHERE username = %s
            """
            cursor.execute(update_query, (file_sha, owner_name))
            db_connection.commit()
            cursor.close()
            db_connection.close()
    except Exception as e:
        logger.error(f"Database error: {e}")
        return render_template("error_page.html")

    return render_template(
        "index.html", message="Congratulations! Take a break while I do the hard work for you"
    )


def create_readme_file(github_username, github_token):
    """Create a README file in the repository."""
    readme_body = {
        "message": configs.FIRST_COMMIT_MESSAGE,
        "content": base64.b64encode(configs.FIRST_COMMIT_CONTENT.encode()).decode(),
    }
    headers = {"Authorization": f"Bearer {github_token}"}
    readme_url = (
        f"{configs.GITHUB_API_URL}/repos/{github_username}/{configs.HARDCODED_REPOSITORY_NAME}/contents/readme.md"
    )
    logger.info(f"Creating README file at {readme_url}")
    return requests.put(readme_url, headers=headers, json=readme_body)


def do_random_commit_on_readme_file(github_username, github_token, file_sha):
    """Make a dummy commit to the README file."""
    commit_body = {
        "message": configs.FIRST_COMMIT_MESSAGE,
        "content": base64.b64encode(configs.FIRST_COMMIT_CONTENT.encode()).decode(),
        "sha": file_sha,
    }
    headers = {"Authorization": f"Bearer {github_token}"}
    commit_url = (
        f"{configs.GITHUB_API_URL}/repos/{github_username}/{configs.HARDCODED_REPOSITORY_NAME}/contents/readme.md"
    )
    response = requests.put(commit_url, headers=headers, json=commit_body)
    if response.status_code == 200:
        logger.info(f"Successfully made a dummy commit for user {github_username}")
    else:
        logger.error(f"Failed to make a dummy commit for user {github_username}: {response.status_code}")


def run_the_schedule_script():
    """Fetch active users and make dummy commits."""
    try:
        db_connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=os.environ.get("MYSQL_PORT"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        if db_connection.is_connected():
            logger.info("Connected to MySQL Database")
            cursor = db_connection.cursor()
            fetch_query = "SELECT username, token, file_sha FROM all_registered_users WHERE is_active = 1"
            cursor.execute(fetch_query)
            results = cursor.fetchall()
            for result in results:
                git_username, encrypted_token, file_sha = result
                git_token = crypt.decrypt(encrypted_token.encode()).decode()
                do_random_commit_on_readme_file(git_username, git_token, file_sha)
            cursor.close()
            db_connection.close()
    except Exception as e:
        logger.error(f"Database error: {e}")


# Schedule the script to run daily at 12:00 AM JST
schedule.every().day.at("12:00").do(run_the_schedule_script)


def run_schedule():
    """Run the scheduler in a separate thread."""
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Start the scheduler thread
    schedule_thread = threading.Thread(target=run_schedule, daemon=True)
    schedule_thread.start()

    # Start the Flask app
    app.run(port=3009, host="0.0.0.0")
