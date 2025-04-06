# ai-dating-bias-analysis

# 💘 AI Dating Bias Analysis

This project investigates how different dating themes — emotional vulnerability, family values, and status/surface-level factors — trigger positive or negative sentiment in online conversations. It was built as part of a speculative AI dating prototype to explore hidden patterns in what people really want (and fear) in romantic relationships.

---

## 🧠 Project Summary

We scraped ~450 posts across dating subreddits and categorized them into three themes using keyword matching:

- 💔 **Emotional Themes** – e.g., ghosting, vulnerability, trust
- 👶 **Family & Future** – e.g., marriage, children, long-term planning
- 💸 **Surface/Status** – e.g., looks, salary, height, jobs

Then we used **VADER Sentiment Analysis** to analyze sentiment polarity for each post and theme.

Finally, we visualized the results using a **box-and-whisker plot** to compare which topics had the most emotional volatility — aka, which ones are most likely to spark polarized conversations.

---

## 🗂️ Files Included

- `reddit_scraper.py` — Scrapes posts from relevant subreddits using PRAW.
- `theme_sentiment_analysis.py` — Cleans and processes posts, categorizes themes, runs sentiment analysis, and generates visual output.
- `reddit_dating_posts.csv` — Raw scraped data.
- `reddit_theme_sentiments.csv` — Theme + sentiment breakdown per post.
- `sentiment_by_theme.png` — Final box plot visualization.

---

## 🔧 How to Run

### Requirements
Install the necessary packages:

```bash
pip install pandas matplotlib seaborn vaderSentiment praw
