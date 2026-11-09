# CareerPilot AI — Development Log

Use this document to record what you actually did. Add dates and be honest about which steps were completed, what AI tools helped, and what you personally tested.

## Project goal

Build an AI-assisted career research application that helps students discover, evaluate, and organize internship and entry-level opportunities.

## Development environment

- Computer: Mac
- Operating system: macOS
- Python version: Python 3
- Editor: TextEdit and Mac Terminal
- AI coding assistant: ChatGPT
- Libraries / APIs: Streamlit, OpenAI API, Python

## Work sessions

### Session 1 — Setup
- Date: November 2026
- What I installed: Python, Streamlit, and the required project libraries.
- Prompts or instructions I gave the AI coding assistant: I asked ChatGPT to help me create a beginners-friendly AI career assistant website for college students.
- What worked: I successfully set up the project, launched the website, and connected it to the OpenAI API.
- Problems encountered: Setting up the project folder, installing libraries, and configuring the API key.
- How I fixed them: I followed step-by-step instructions from ChatGPT and corrected the setup until the website launched successfully.
- What I learned: How to use Python, Terminal, Streamlit, and an API to create an AI-powered application.

### Session 2 — Application interface
- Date: November 2026
- Features implemented: Created the Discover page, job matching system, job analysis tool, application tracker, resume assistant, and navigation sections.
- Prompts or instructions used: I asked ChatGPT to help build a career website with tools that help college students find and evaluate job opportunities.
- Problems encountered: Making sure the website displayed correctly and that each feature worked properly.
- How I tested the features: I opened the website in Safari, viewed sample job listings, analyzed a job description, saved an opportunity, and updated its application status.
- What I learned:How to organize a website into different sections and use Python and Streamlit to make interactive features.

### Session 3 — AI functionality
- Date: November 2026 
- API/model used: OpenAI API using GPT-4.1-mini.
- What the AI feature does: Analyzes job descriptions, identifies matching skills and skill gaps, improves resume bullet points, drafts cover letters, and researches career opportunities.
- How I checked the output: I tested the job analysis feature with an IT Support Intern description and reviewed the generated recommendations. I also tested the resume assistant and Career Agent.
- Limitations or errors: AI-generated information may not always be accurate. Job listings need to be verified, and resume or cover letter suggestions need to be reviewed before use.
- What I learned: How an API connects an application to an AI model and how AI can help users research careers and prepare for employment.

### Session 4 — External integration
- Date: November 2026
- External application connected: None. Google Sheets integration is available as an optional feature but was not configured.
- Data sent: No data was sent to an external application.
- Permissions/configuration required: Google Cloud setup, Google Sheets API access, and service account credentials would be required.
- What I tested: I reviewed the optional Google Sheets integration but did not test a connection.
- Problems encountered: Setting up an external application connection requires additional configuration.
- What I learned: How applications can connect to external services and share information through APIs.

### Session 5 — Final testing
- Date: November 2026
- Test cases: Tested whether the website launches, sample opportunities appear, job descriptions can be analyzed, opportunities can be saved, application statuses can be updated, resume and cover letter drafts can be generated, and the Career Agent produces research results.
- Bugs found: No major problems prevented the application from running. Some setup and API configuration issues occurred during development.
- Fixes: Followed ChatGPT's instructions to correct the setup, configure the API, and get the application running.
- Remaining limitations: AI results may not always be accurate. Live job listings need verification, sample listings are fictional, and Google Sheets integration has not been configured. 
- What I would improve next: Connect Google Sheets, improve the accuracy of job research, add more job sources, and improve the website's design.

### Session 6 — Career Agent upgrade (AI-assisted code update)
- Date: 2026-11-08
- AI coding assistant: ChatGPT
- Features added: a multi-step Career Agent that researches current opportunities with web search, compares results with the candidate profile, and creates a ranked shortlist and action plan. Existing Discover, Analyze a Job, Application Tracker, Resume Assistant, and About sections were preserved.
- Other updates: replaced deprecated Streamlit `use_container_width` arguments with `width="stretch"`; updated the minimum Streamlit version in `requirements.txt`.
- Test completed: Python syntax compilation passed.
- Testing still required: run the app, test the Career Agent with API access, verify job links on employer websites, and check that existing features still work.
- What I learned: AI research results need manual verification; a successful syntax check does not replace testing the app in a browser.

## Example test checklist

- [ ] App starts in demo mode without an API key.
- [x] Sample opportunities appear.
- [ ] Match score changes when profile skills change.
- [x] A listing can be saved to the tracker.
- [x] Tracker status can be updated.
- [x] CSV export works.
- [ ] Missing job description produces a helpful warning.
- [x] AI analysis works when a valid API key is configured.
- [ ] Live research sources are checked manually.
- [ ] Google Sheets export works if configured.

## Reflection for the professor

Write in your own words:
1. What problem does CareerPilot AI solve? - CareerPilot AI helps college students find and evaluate internships and entry-level jobs. It makes it easier to compare job requirements with personal skills, identify areas for improvement, and prepare for applications.
2. Why did you choose this project? - I chose this project because I wanted to create something useful for college students who are preparing to enter the workforce. Since I am studying Computer Information Systems, I was also interested in learning how AI and programming can be used to solve real-world problems.
3. Which parts were created with AI assistance? - I used ChatGPT to help me plan and develop the website, write and improve Python code, troubleshoot errors, and add features. AI assistance helped create the job analysis tool, resume assistant, application tracker, and Career Agent. I also tested the features myself to make sure they worked.
4. What did you understand better after building it? - I better understand how Python can be used to build a website and how an API connects an application to an AI model. I also learned about using if/else statements, loops, and user inputs to make an application interactive.
5. What was the hardest problem? - The hardest part was setting up the project and getting everything to work correctly. I had to learn how to use Mac Terminal, install the required libraries, configure the OpenAI API key, and troubleshoot problems. Taking it one step at a time helped me get the website running.
6. How did you test whether the application worked? - I tested the website by opening it in Safari and trying its different features. I checked the sample job listings, analyzed a job description, saved an opportunity, changed its application status, generated resume and cover letter suggestions, and ran the Career Agent. I reviewed the results to make sure the features were working.
7. What are the application's limitations? - CareerPilot AI may sometimes generate inaccurate information, so users should verify job listings and AI recommendations. The sample job listings are fictional, the job match scores are estimates, and the Google Sheets integration has not been configured. Users should also review resume and cover letter drafts before using them.
8. What would you build next? - In the future, I would improve CareerPilot AI by connecting it to Google Sheets, adding more reliable job sources, improving job matching, and creating more features to help students prepare for interviews and find internships. I would also improve the website's design and make it easier to use.
