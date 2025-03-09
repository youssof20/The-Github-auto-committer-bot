# Green GitHub == $500k Job? 💰

## Inspiration

I came across this super viral [Tweet](https://x.com/RhysSullivan/status/1873104145709973624) where someone allegedly landed a **$500k job** without any interview—just because they had a **fully green GitHub commit history**. Sounds crazy, right? But hey, why not give it a shot? That's why I built this **GitHub Auto Committer Bot**.

---

## What Does This Repo Do?

1. **Simulates an All-Green GitHub Commit Graph**: Keeps your GitHub contribution graph glowing green.
2. **Automates Daily Commits**: Makes a commit to your GitHub account every single day.
3. **Private Repository**: All commits are made to a private repository, so no one sees the actual code—just your activity.
4. **Look Like a Pro**: Helps you appear as a highly active and dedicated coder. 😎

---

## How It Works

### Prerequisites
1. **GitHub Classic Token**: You’ll need a GitHub Classic Token with **read and write permissions** for repositories. [Here’s how to create one](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

### Steps
1. **Register Your Token**:
   - Provide your GitHub token to the application.
   - The app will create a **private repository** in your account (this counts as your first commit).
   - A `README.md` file will also be created in the repository.

2. **Daily Commits**:
   - The app stores your token securely (encrypted, of course) in a database.
   - A scheduled job runs every day at **12:00 AM JST** to make a dummy commit to your `README.md` file.
   - This ensures your GitHub activity stays green without any manual effort.

---

## Does It Actually Work?

Honestly, I haven’t tested it enough to guarantee a $500k job. But it’s a fun experiment, and at the very least, it’ll make your GitHub profile look impressive! 🚀

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/github-auto-committer.git
cd github-auto-committer
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add the following variables:
```env
FERNET_KEY=your_fernet_key
MYSQL_HOST=your_mysql_host
MYSQL_PORT=your_mysql_port
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_mysql_database
GITHUB_API_URL=https://api.github.com
HARDCODED_REPOSITORY_NAME=auto-committer
FIRST_COMMIT_MESSAGE="Initial commit"
FIRST_COMMIT_CONTENT="This is a dummy commit to keep your GitHub green!"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Web Interface
Open your browser and go to `http://localhost:3009`. Enter your GitHub token to get started.

---

## Disclaimer

This project is **just for fun**! While it might make your GitHub profile look amazing, there’s no guarantee it’ll land you a $500k job. Use it at your own risk, and enjoy the green squares! 🟩
