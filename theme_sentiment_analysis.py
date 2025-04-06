import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import re

# Emoji support
plt.rcParams['font.family'] = 'Segoe UI Emoji'  # Use "Apple Color Emoji" on macOS

# --- Load Reddit data ---
df = pd.read_csv("reddit_dating_posts.csv")
df["full_text"] = df["title"].fillna("") + " " + df["text"].fillna("")

# --- Define themes ---
themes = {
    "💔 Emotional Themes": ["ghost", "ghosting", "narcissist", "narcissism", "trust", "honesty", "vulnerable"],
    "👶 Family & Future": ["kids", "children", "family", "parent", "father", "mother", "marriage", "husband", "wife"],
    "💸 Surface/Status": ["money", "salary", "job", "career", "looks", "height", "weight", "attractive"]
}

# --- Initialize sentiment analyzer ---
analyzer = SentimentIntensityAnalyzer()

# --- Sentiment tracking per theme ---
theme_sentiment = {
    theme: {"pos": 0, "neg": 0, "neu": 0, "total": 0}
    for theme in themes
}

# --- Score posts by theme ---
theme_posts = []
for _, row in df.iterrows():
    text = row["full_text"].lower()
    for theme, keywords in themes.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", text) for keyword in keywords):
            sentiment = analyzer.polarity_scores(text)
            theme_sentiment[theme]["pos"] += sentiment["pos"]
            theme_sentiment[theme]["neg"] += sentiment["neg"]
            theme_sentiment[theme]["neu"] += sentiment["neu"]
            theme_sentiment[theme]["total"] += 1
            theme_posts.append({
                "theme": theme,
                "compound": sentiment["compound"],
                "text": row["full_text"][:150] + "..."
            })
            break  # only count a post once

# --- Convert to DataFrame ---
theme_posts_df = pd.DataFrame(theme_posts)

# --- Print most negative post per theme ---
for theme in theme_posts_df["theme"].unique():
    theme_df = theme_posts_df[theme_posts_df["theme"] == theme]
    most_negative = theme_df.loc[theme_df["compound"].idxmin()]
    print(f"\n🔻 Most Negative for {theme}:\n{most_negative['text']}")

# --- Classify post sentiment ---
def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

theme_posts_df["sentiment_label"] = theme_posts_df["compound"].apply(classify_sentiment)

# --- Plot ---
plt.figure(figsize=(10, 6))
sns.boxplot(
    x="theme",
    y="compound",
    data=theme_posts_df,
    palette="coolwarm",
    width=0.6,
    boxprops=dict(alpha=0.8)
)

# --- Count + label ---
theme_counts = theme_posts_df["theme"].value_counts()
for i, theme in enumerate(theme_counts.index):
    count = theme_counts[theme]
    plt.text(i, 1.05, f"{count} posts", ha='center', fontsize=10, color='black')

# --- Annotate most negative post ---
min_row = theme_posts_df.loc[theme_posts_df["compound"].idxmin()]
plt.annotate(
    "Most Negative Post",
    xy=(list(theme_counts.index).index(min_row["theme"]), min_row["compound"]),
    xytext=(0, 40),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->", lw=1.5),
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9)
)

# --- Titles and labels ---
plt.suptitle("Analyzing Sentiment Trends in Dating Conversations", fontsize=10, y=0.98)
plt.axhline(0, color="gray", linestyle="--")
plt.title("Sentiment Distribution by Theme")
plt.ylabel("Sentiment Score\n(-1 = Strongly Negative, +1 = Strongly Positive)")
plt.xticks(rotation=45, ha="right")
plt.figtext(0.5, -0.05, "Based on ~450 Reddit posts from r/dating, r/OkCupid, r/hingeapp, etc.",
            wrap=True, horizontalalignment='center', fontsize=9)
plt.tight_layout()

# --- Save + Show ---
plt.savefig("sentiment_by_theme.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Export CSV ---
theme_posts_df_export = theme_posts_df.copy()
theme_posts_df_export["theme"] = theme_posts_df_export["theme"].str.title()
theme_posts_df_export.to_csv("reddit_theme_sentiments.csv", index=False)

# --- Print counts ---
print("\n🧠 Post Counts by Theme")
for theme, scores in theme_sentiment.items():
    print(f"{theme:<20}: {scores['total']} posts")


