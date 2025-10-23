import feedparser
import pandas as pd
from datetime import datetime
from dateutil import parser as dateparser
import os

# ---- CONFIGURATION ----
KEYWORDS = [
    # Core entities
    "Independent System and Market Operator",
    "ISMO Pakistan",
    "Power Division Pakistan",
    "NEPRA",
    "Central Power Purchasing Agency", 

    # Market reform concepts
    "Competitive Trading Bilateral Contract Market",
    "CTBCM",
    "Electricity Market",
    "Power Market Reforms",
    "Wholesale Electricity Market",

    # Governance & regulatory codes
    "Market Commercial Code",
    "Grid Code",
    "Dispatch Code",
    "Market Surveillance and Monitoring Framework",

    # Policy & planning
    "National Electricity Plan",
    "Indicative Generation Capacity Expansion Plan",
    "Transmission System Expansion Plan",
    "Circular Debt Management Plan"
]

OUTPUT_FILE = "ismo_articles.csv"

from datetime import datetime
from dateutil import parser as dateparser
import feedparser
import pandas as pd
import os

# ---- CONFIGURATION ----
CUTOFF_DATE = datetime(2025, 9, 1) 

def fetch_articles(keyword):
    """Fetch articles from Google News RSS for a given keyword"""
    rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en&gl=PK&ceid=PK:en"
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries:
        published_date = None
        if "published" in entry:
            try:
                published_date = dateparser.parse(entry.published)

                # Make timezone-naive to match CUTOFF_DATE
                if published_date.tzinfo is not None:
                    published_date = published_date.replace(tzinfo=None)
            except Exception:
                published_date = None

        # Apply recency filter safely
        if published_date and published_date >= CUTOFF_DATE:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": published_date.strftime("%Y-%m-%d"),
                "keyword": keyword
            })

    return articles

# ---- MAIN LOGIC ----
def main():
    all_articles = []

    # Fetch new articles for each keyword
    for kw in KEYWORDS:
        print(f"🔍 Searching for: {kw}")
        articles = fetch_articles(kw)
        all_articles.extend(articles)

    # Convert to DataFrame
    df_new = pd.DataFrame(all_articles)
    print(f"📋 {len(df_new)} total recent articles fetched across all keywords.")

    # Combine with existing CSV if available
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        try:
            df_old = pd.read_csv(OUTPUT_FILE)
            combined = pd.concat([df_old, df_new]).drop_duplicates(subset=["link"])
        except pd.errors.EmptyDataError:
            print("Existing CSV is empty — starting fresh.")
            combined = df_new
    else:
        combined = df_new

    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved {len(combined)} total unique articles to {OUTPUT_FILE}")

    # Show a preview
    print(df_new.head())

    # ✅ Return all articles for alert script
    return all_articles


if __name__ == "__main__":
    main()
