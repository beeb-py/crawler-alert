import feedparser
import pandas as pd
from datetime import datetime
import os

# ---- CONFIGURATION ----
KEYWORDS = [
    "Independent System and Market Operator",
    "ISMO Pakistan",
    "Power Division",
    "electricity market",
    "energy reforms",
    "Competitive Trading Bilateral Contract Market",
    "CTBCM",
    "power sector reforms",
    "electricity market liberalization",
    "single buyer model Pakistan",
    "wholesale electricity market Pakistan",
    "market operator Pakistan energy",
    "system operator Pakistan power sector",
    "dispatch code Pakistan",
    "market code NEPRA",
    "auction framework",
    "Central Power Purchasing Agency",
    "National Electric Power Regulatory Authority",
    "Power Division Pakistan",
    "Ministry of Energy Power Division",
    "NTDC Pakistan",
    "DISCO reforms Pakistan",
    "K-Electric market participation",
    "IPP contracts Pakistan",
    "electricity demand forecast Pakistan",
    "generation capacity Pakistan",
    "renewable energy integration Pakistan",
    "transmission planning Pakistan",
    "grid modernization Pakistan",
    "energy transition Pakistan",
    "carbon markets Pakistan",
    "power system reliability Pakistan",
    "capacity payments Pakistan",
    "merit order Pakistan",
    "load shedding Pakistan",
    "electricity tariff hike Pakistan",
    "circular debt Pakistan",
    "electricity reforms",
    "Market Commercial Code",
    "Grid Code",
    "Distribution Code",
    "Metering Code",
    "Dispatch Code",
    "Connection Code",
    "Indicative Generation Capacity Expansion Plan (IGCEP)",
    "Transmission System Expansion Plan (TSEP)",
    "National Electricity Plan (NEP)",
    "Renewable Energy Policy",
    "Energy Efficiency and Conservation Policy",
    "Electricity Act (Amended)",
    "NEPRA Act (Amendment 2018)",
    "Market Surveillance and Monitoring Framework",
    "License for Market Operator",
    "License for System Operator",
    "Circular Debt Management Plan (CDMP)",
    "National Energy Policy"
]

OUTPUT_FILE = "ismo_articles.csv"

# ---- HELPER FUNCTION ----
def fetch_articles(keyword):
    """Fetch articles from Google News RSS for a given keyword"""
    rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en&gl=PK&ceid=PK:en"
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if "published" in entry else "N/A",
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
    print(f"📋 {len(df_new)} total articles fetched across all keywords.")

    # Combine with existing CSV if available
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        try:
            df_old = pd.read_csv(OUTPUT_FILE)
            combined = pd.concat([df_old, df_new]).drop_duplicates(subset=["link"])
        except pd.errors.EmptyDataError:
            print("⚠️ Existing CSV is empty — starting fresh.")
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
