import os
import openai
import gspread
import pandas as pd
import smtplib
import requests
import matplotlib.pyplot as plt
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk.webhook import WebhookClient
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load .env
load_dotenv()

# 1. Config
openai.api_key = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIAL_FILE  = os.getenv("GOOGLE_CREDENTIAL_FILE")

# 2. Kết nối Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIAL_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1
data = pd.DataFrame(sheet.get_all_records())

# 3. Google Drive Service
drive_service = build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path, filename):
    file_metadata = {'name': filename, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    return file.get('webViewLink')

# 4. Log DB
conn = sqlite3.connect("task_log.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (
    timestamp TEXT, task TEXT, status TEXT, details TEXT)''')
conn.commit()

def log_task(task, status, details=""):
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (str(datetime.now()), task, status, details))
    conn.commit()

def send_slack(msg):
    WebhookClient(SLACK_WEBHOOK).send(text=msg)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

# 5. Xử lý từng task
def process_row(row):
    try:
        desc = row["description"]
        fmt = row["output_format"].lower()
        model = row["model"].lower()

        filename = f"{desc.replace(' ', '_')}.{fmt}"
        file_path = f"temp/{filename}"

        if model == "openai":
            if fmt in ["png", "jpg", "pdf", "png"]:
                raise Exception(f"Unsupported format: {fmt}")
                response = openai.Image.create(prompt=desc, n=1, size="512x512")
                image_url = response['data'][0]['url']
                content = requests.get(image_url).content
                with open(file_path, "wb") as f:
                    f.write(content)
            elif fmt == "mp3":
                speech = openai.Audio.speech.create(model="tts-1", input=desc, voice="alloy")
                with open(file_path, "wb") as f:
                    f.write(speech.content)
            else:
                raise Exception(f"Unsupported format: {fmt}")
        else:
            raise Exception("Model not supported yet.")

        drive_url = upload_to_drive(file_path, filename)
        log_task(desc, "Success", f"File uploaded: {drive_url}")
        send_slack(f"Success: {desc}")
    except Exception as e:
        log_task(desc, "Fail", str(e))
        send_slack(f"Failed: {desc}")
        send_email("Automation Failed", f"{desc}\n\n{e}")

# 6. Chạy toàn bộ task
os.makedirs("temp", exist_ok=True)
for _, row in data.iterrows():
    process_row(row)

# 7. Báo cáo hằng ngày
def generate_daily_report():
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    today = pd.to_datetime(df["timestamp"]).dt.date == datetime.today().date()
    df_today = df[today]
    success = df_today[df_today["status"] == "Success"].shape[0]
    fail = df_today[df_today["status"] == "Fail"].shape[0]

    plt.figure(figsize=(5,5))
    plt.pie([success, fail], labels=["Success", "Fail"], autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Today's Summary")
    plt.savefig("daily_report.png")

    report_url = upload_to_drive("daily_report.png", "daily_report.png")
    body = f"Success: {success}\nFail: {fail}\n\nReport: {report_url}"
    send_email("Daily Automation Report", body)

generate_daily_report()