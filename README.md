# Simple Website Crawler

This project automatically crawls news articles using **Google News RSS** feeds. It detects newly published articles containing keywords and sends automated email alerts to subscribed recipients.

---

## Features
- Crawls news articles via Google News RSS.
- Filters results based on predefined **keywords**.
- Automatically detects and saves **only new articles** to a CSV file.
- Sends **email alerts** summarizing newly found articles.
- Runs on a schedule using **GitHub Actions.**

---

## Project Structure
- crawler-alert/
- crawler.py # Handles fetching and saving of news articles
- crawler_alert.py # Compares new vs old results and sends email alerts
- requirements.txt # Python dependencies
- .env # Local environment variables (not committed to Git)

---

## Setup Instructions

### 1. Clone the Repository
git clone https://github.com/beeb-py/crawler-alert.git
cd crawler-alert

### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Create a .env File
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password (acquired via Google Apps)
RECEIVER_EMAIL=recipient_email@gmail.com


