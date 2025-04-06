import praw
import pandas as pd
from datetime import datetime

# --- Fill these with your Reddit API info ---
REDDIT_CLIENT_ID = 'c1iDMD3y0yqNP9TZ1oNFNw'
REDDIT_SECRET = 'fIMkDig7rtUEYXQw4FMYUr1Nu71RdA'
REDDIT_USER_AGENT = 'dating-bias-scraper by u/What-Lives'

# --- Connect to Reddit ---
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# --- Subreddits and post limit ---
subreddits = ["datingoverthirty", "dating", "relationships", "OkCupid", "hingeapp"]
limit = 100

# --- Storage for post data ---
posts_data = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    print(f"📥 Scraping r/{sub}...")

    for post in subreddit.hot(limit=limit):
        # Skip sticky threads and posts with no text
        if post.stickied or not post.selftext.strip():
            continue

        posts_data.append({
            "subreddit": sub,
            "title": post.title,
            "text": post.selftext,
            "flair": post.link_flair_text,
            "upvotes": post.score,
            "comments": post.num_comments,
            "created_utc": datetime.utcfromtimestamp(post.created_utc)
        })

# --- Create DataFrame ---
df = pd.DataFrame(posts_data)

# --- Save to CSV ---
df.to_csv("reddit_dating_posts.csv", index=False)
print(f"✅ Scraped {len(df)} posts across {len(subreddits)} subreddits.")

