import praw
import random

reddit = praw.Reddit(
    client_id="r9RGT6ulitbV65Otk0qHHQ",
    client_secret="QvJHP-1uIv7OEL5z0YPYA7wcZXq-Yg",
    password="Andre91109",
    user_agent="gus_discord_bot",
    username="Interesting-Luck2051",
)

# random_subreddit = str(reddit.random_subreddit(nsfw=True))
# print(random_subreddit)        



# print(str(reddit.random_subreddit())) #set paramater to nsfw=True for nsfw




def find(sr):
    subreddit = reddit.subreddit(sr)
    extensions_to_check = [".gif", ".jpg", ".png", ".mp4"]
    results = []
    for submission in subreddit.hot(limit=50):
        if not submission.stickied:
            if any(substring in submission.url for substring in extensions_to_check):
                # print(submission.url)
                results.append(submission.url)
    return results



