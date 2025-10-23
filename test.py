from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"), os.getenv("RECEIVER_EMAIL"))
