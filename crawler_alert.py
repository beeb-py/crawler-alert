import os
import pandas as pd
from datetime import datetime
from crawler import main as run_crawler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv  

# Load .env file
load_dotenv()

# ====================
# EMAIL CONFIG
# ====================
EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")
EMAIL_RECEIVER = os.getenv("RECEIVER_EMAIL")

# ====================
# FILE PATHS
# ====================
CURRENT_CSV = "ismo_articles.csv"
PREVIOUS_CSV = "ismo_articles_previous.csv"

# ====================
# FUNCTION: SEND EMAIL
# ====================
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ====================
# MAIN WORKFLOW
# ====================
def main():
    print("🔍 Running article crawler...")
    current_articles = run_crawler()
    
    # Convert to DataFrame
    current_df = pd.DataFrame(current_articles)
    print(f"📋 {len(current_df)} total articles fetched.")
    
    # Handle first run or missing files
    if not os.path.exists(PREVIOUS_CSV):
        print("🆕 First run or missing previous data — creating initial CSVs.")
        current_df.to_csv(CURRENT_CSV, index=False)
        current_df.to_csv(PREVIOUS_CSV, index=False)
        send_email(
            subject="[Crawler] Initial Article Snapshot Created",
            body=f"The crawler ran for the first time and found {len(current_df)} total articles.\n\nNo comparison was done since no previous data existed."
        )
        return

    # Load previous snapshot
    previous_df = pd.read_csv(PREVIOUS_CSV)

    # Find new articles by link
    new_articles = current_df[~current_df["link"].isin(previous_df["link"])]

    # Save current as new snapshot
    current_df.to_csv(CURRENT_CSV, index=False)

    # Move current -> previous for next run
    current_df.to_csv(PREVIOUS_CSV, index=False)

    # Reporting
    if new_articles.empty:
        print("ℹ️ No new articles found.")
        send_email(
            subject="[Crawler] No New Articles Found",
            body="The crawler ran successfully, but no new articles were detected today."
        )
    else:
        print(f"🆕 Found {len(new_articles)} new articles!")
        # Prepare email body
        article_list = "\n\n".join(
            [f"{row['title']}\n{row['link']}" for _, row in new_articles.iterrows()]
        )
        email_body = (
            f"{len(new_articles)} new articles found at {datetime.now()}:\n\n"
            f"{article_list}"
        )

        send_email(
            subject=f"[Crawler] {len(new_articles)} New Articles Found",
            body=email_body,
        )

    print("✅ Crawler + Email process completed successfully.\n")

# ====================
# ENTRY POINT
# ====================
if __name__ == "__main__":
    main()
