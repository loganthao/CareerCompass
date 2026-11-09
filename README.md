# CareerPilot AI

A beginner-friendly AI career research workspace built with Python and Streamlit.

## What it does

- Collects a student's career profile and preferences.
- Shows clearly labeled fictional sample listings for testing.
- Calculates a transparent keyword-overlap match estimate.
- Uses the OpenAI API for job-description analysis and resume/cover-letter drafts.
- Includes a multi-step Career Agent that researches live openings, compares them with a student profile, and creates an action plan.
- Can use web search through the OpenAI Responses API for live opportunity research.
- Tracks selected opportunities and exports them to CSV.
- Optionally appends tracker entries to Google Sheets using a Google service account.

## Important

- Sample job listings are fictional examples, not real openings.
- Live research results must be verified at the employer's official career page.
- API usage is billed separately from a ChatGPT subscription.
- Do not commit API keys, Google service-account JSON files, or personal data to GitHub.
- The app does not submit job applications or send emails.

## 1. Install prerequisites

Install:
- Python 3.11 or newer
- Visual Studio Code (optional but recommended)

Download Python: https://www.python.org/downloads/macos/

## 2. Open the project folder in Terminal

Move into the folder containing `app.py`, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run the app in demo mode

```bash
streamlit run app.py
```

The app opens in your browser. Demo mode does not require an API key.

## 4. Enable AI features (optional)

Create an API key at https://platform.openai.com/api-keys and make sure API billing/access is configured.

You can paste the key into the password field in the app sidebar. It is held in the current app session and is not saved to a file by this project.

Alternatively, copy `.env.example` to `.env` and place your key there. Keep `.env` private and never upload it to GitHub.

The default model is `gpt-4.1-mini`. If that model is unavailable to your API account, change the Model field in the sidebar to a model you can access.

Live research uses the OpenAI Responses API web search tool. Tool availability and model access depend on your API account.

## 5. Optional Google Sheets integration

1. Create a Google Cloud project.
2. Enable the Google Sheets API and Google Drive API.
3. Create a service account and download its JSON key.
4. Put the JSON file in the project folder and name it `google_service_account.json`.
5. Create a Google spreadsheet.
6. Share the spreadsheet with the service account's email address as an Editor.
7. Copy the spreadsheet ID from its URL.
8. In the app's Application Tracker tab, enter the spreadsheet ID and credentials file path, then select Save tracker to Google Sheets.

Never share the JSON key or commit it to source control. The `.gitignore` file excludes it.

## 6. Suggested demonstration

1. Open Discover and load sample opportunities.
2. Show the baseline match score and matching/missing skill lists.
3. Save a sample opportunity to the tracker.
4. Change its application status.
5. Export the tracker to CSV.
6. If API access is configured, analyze a job description and generate a resume/cover-letter draft.
7. Run the Career Agent to research current openings and produce a personalized comparison and action plan.
8. Verify every result on the employer's official career page before applying.

## Project structure

```text
CareerPilot-AI/
├── app.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_LOG.md
├── .env.example
└── .gitignore
```
