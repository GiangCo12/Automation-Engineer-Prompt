# AUTOMATION ENGINEER & AI PROMPT ENGINEERING PROJECT

## 🔥 OVERVIEW

This project is divided into two parts:

- **Assignment #1: Automation Workflow**
- **Assignment #2: AI Prompt Engineering**

It automates content generation from Google Sheets using AI models, uploads results to Google Drive, sends notifications via Slack and Email, logs to SQLite, and generates daily reports with visualization.

---

## 🚀 PROJECT STRUCTURE
<img width="638" alt="Image" src="https://github.com/user-attachments/assets/2956af8e-0d18-4f10-80d3-5993c4ff8ed1" /> 

## 🛠 TECHNOLOGIES USED

- Python 3.11
- Google Sheets API
- Google Drive API
- OpenAI API (DALL·E, TTS)
- Slack Webhook API
- smtplib (Email Notifications)
- SQLite3 (Logging database)
- Matplotlib (Chart for daily report)
****

##  PREPARE YOUR ENVIRONMENT:

- GOOGLE_SHEET_ID=your_google_sheet_id
- GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
- OPENAI_API_KEY=your_openai_api_key
- SLACK_WEBHOOK_URL=your_slack_webhook_url
- EMAIL_SENDER=your_email
- EMAIL_PASSWORD=your_app_password
- EMAIL_RECEIVER=receiver_email
- GOOGLE_CREDENTIAL_FILE=your_service_account.json

📚 ASSIGNMENT #1: AUTOMATION WORKFLOW

🔥 Features Implemented:

	•	Read Tasks from Google Sheets
	•	Generate Content (Image/Audio) using OpenAI (DALL·E, TTS)
	•	Upload Outputs to a specific Google Drive folder
	•	Send Notifications via Slack and Email
	•	Log all activities into a local SQLite Database (task_log.db)
	•	Generate Daily Reports with a pie chart summarizing task statuses

🧩 Main Python Libraries Used:

	•	gspread
	•	google-auth
	•	google-auth-oauthlib
	•	openai
	•	slack_sdk
	•	smtplib
	•	sqlite3
	•	matplotlib
	•	dotenv
	•	os, shutil, time, datetime, pandas

🖼 Sample Automation Output:

Generated image:

📚 ASSIGNMENT #2: AI PROMPT ENGINEERING

🔥 Prompt Strategy:

	•	Designed Effective Prompts for DALL·E to generate high-quality images
	•	Tested Variations with different prompt engineering techniques (specificity, context, styles)
	•	Evaluated Outputs and refined prompts accordingly

✏️ Example Prompts Used:

	•	“A futuristic city at sunset in cyberpunk style, ultra-detailed, 8K resolution.”
	•	“A cute cat playing a guitar, Pixar-style 3D rendering, cheerful mood.”

🖼 Generated Images:

See in Question2/images_generated/ folder!

🧠 CHALLENGES FACED

	•	Google API Authorization Issues: Solved by using a Service Account and .json key file.
	•	File Size Limits in GitHub: Addressed by excluding large video files from Git history.
	•	API Quotas and Timeouts: Implemented retry mechanisms and error handling.
	•	Unsupported format errors: Resolved by validating input data formats properly before sending requests.

 💡 SUGGESTIONS FOR FUTURE IMPROVEMENT

	•	Implement Retry Logic for OpenAI and Google APIs to improve reliability.
	•	Enhance Dashboard with more detailed analytics (bar charts, trends over days).
	•	Deploy Automation to a server (e.g., AWS Lambda, GCP Cloud Functions) for daily scheduled runs.
	•	Use Git Large File Storage (LFS) if handling large media files in the future.

 📢 FINAL OUTCOME

Successfully built a full-stack Automation Workflow + applied AI Prompt Engineering to generate content automatically.
Project fully documented, ready for production or further enhancements.
