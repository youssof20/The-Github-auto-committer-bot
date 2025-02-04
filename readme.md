# Green Github == $500k Job  💰
Inspiration : I read this super viral [Tweet](https://x.com/RhysSullivan/status/1873104145709973624) that said someone allegedly landed a $500k job without any job interview - just because they had a fully green Github commit history.
I know it sounds absurd but I thought why not take a chance and replicate it for my own profile.

That's why I built this Github Auto Committer bot.

# What this repo does ?
1. Simulates an all-green Github commit graph.
2. Automates daily commit to Github.
3. All this is done behind a private repository so people only see your commits but not the actual code behind it.
4. Above all, helps you look like a really cool coder :)

# How it works ?
1. You will need a Github Classic Token for this. Please ensure that the token has read and write permission for the repository.
2. The first you register in the application, I will create a new private repository in your account using the Token that you have provided. This will count as your first commit.
3. At the same time, I will create a readme.md file in your new private repository.
4. I will store the token ( goes without saying its encrypted ) in a database. I have a scheduled job which runs at 12 AM JST which reads the token and makes a dummy commit to your readme.md file. This is how you get a daily commit on your account.

## Does it actually work ?
I dont know - never got the chance to test it enough. But hopefully it will.

## Disclaimer

This repo is just for fun! No guarantees of a $500K job, but hey, it might at least make your profile look good. 🚀
