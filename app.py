import os
import re
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CareerCompass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Demo data: illustrative only.
# These are not real job openings.
# -----------------------------
DEMO_JOBS = [
    {
        "company": "Sample Technology Group",
        "title": "IT Support Intern",
        "location": "Fresno, CA",
        "work_mode": "On-site",
        "type": "Internship",
        "skills": "troubleshooting, customer service, Windows, communication, networking",
        "description": (
            "Illustrative training listing. Assist staff with basic hardware and software "
            "troubleshooting, document support tickets, help users with account access, "
            "and learn basic networking concepts. Strong communication and customer "
            "service skills are helpful. No professional IT experience required."
        ),
        "url": "https://example.com/sample-it-support-intern",
    },
    {
        "company": "Sample Analytics Studio",
        "title": "Junior Data Analyst Intern",
        "location": "Remote",
        "work_mode": "Remote",
        "type": "Internship",
        "skills": "Excel, SQL, data analysis, reporting, attention to detail",
        "description": (
            "Illustrative training listing. Help clean spreadsheets, prepare basic reports, "
            "identify trends, and communicate findings. Familiarity with Excel is useful; "
            "SQL coursework or project experience is a plus."
        ),
        "url": "https://example.com/sample-data-analyst-intern",
    },
    {
        "company": "Sample Business Systems Co.",
        "title": "Business Systems Assistant",
        "location": "Fresno, CA / Hybrid",
        "work_mode": "Hybrid",
        "type": "Entry-level",
        "skills": "business processes, documentation, Excel, communication, problem solving",
        "description": (
            "Illustrative training listing. Support business application users, document "
            "workflow issues, help test system updates, and coordinate with technical and "
            "business teams. Strong organization and communication are important."
        ),
        "url": "https://example.com/sample-business-systems-assistant",
    },
]

def get_api_key():
    # The key is entered for the current session only; it is not written to disk.
    return st.session_state.get("openai_api_key", "").strip() or os.getenv("OPENAI_API_KEY", "").strip()

def get_openai_client():
    key = get_api_key()
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception as exc:
        st.error(f"Could not initialize the OpenAI client: {exc}")
        return None

def clean_list(text):
    return [item.strip() for item in re.split(r"[,;\n]", text or "") if item.strip()]

def calculate_match(profile, job):
    """Transparent baseline score using skill and preference overlap."""
    skills = [s.lower() for s in clean_list(profile.get("skills", ""))]
    job_text = " ".join([
        job.get("title", ""),
        job.get("description", ""),
        job.get("skills", ""),
    ]).lower()

    if not skills:
        skill_score = 0
        matched = []
        missing = []
    else:
        matched = [s for s in skills if s in job_text]
        missing = [s for s in skills if s not in job_text]
        skill_score = round((len(matched) / len(skills)) * 70)

    location_pref = profile.get("location", "").strip().lower()
    job_location = (job.get("location", "") + " " + job.get("work_mode", "")).lower()
    location_score = 20 if not location_pref or location_pref in job_location or "remote" in job_location else 5

    desired_type = profile.get("desired_type", "Any")
    type_score = 10 if desired_type == "Any" or desired_type.lower() in job.get("type", "").lower() else 4

    total = min(100, skill_score + location_score + type_score)
    return total, matched, missing

def ai_response(prompt, use_web_search=False):
    client = get_openai_client()
    if client is None:
        return None, "Add an OpenAI API key in the sidebar to enable live AI features. Demo mode still works."
    try:
        kwargs = {
            "model": st.session_state.get("model_name", "gpt-4.1-mini"),
            "input": prompt,
        }
        if use_web_search:
            kwargs["tools"] = [{"type": "web_search"}]
        response = client.responses.create(**kwargs)
        return response.output_text, None
    except Exception as exc:
        return None, f"AI request failed: {exc}"

def save_to_google_sheets(rows, sheet_id, credentials_path):
    try:
        import gspread
        gc = gspread.service_account(filename=credentials_path)
        spreadsheet = gc.open_by_key(sheet_id)
        try:
            worksheet = spreadsheet.worksheet("CareerPilot Tracker")
        except Exception:
            worksheet = spreadsheet.add_worksheet(title="CareerPilot Tracker", rows=200, cols=12)

        headers = [
            "Date Added", "Company", "Job Title", "Location", "Work Mode",
            "Type", "Match Score", "Status", "URL", "Notes"
        ]
        existing = worksheet.row_values(1)
        if not existing:
            worksheet.append_row(headers)

        values = []
        for row in rows:
            values.append([
                row.get("date_added", datetime.now().strftime("%Y-%m-%d")),
                row.get("company", ""),
                row.get("title", ""),
                row.get("location", ""),
                row.get("work_mode", ""),
                row.get("type", ""),
                str(row.get("match_score", "")),
                row.get("status", "Interested"),
                row.get("url", ""),
                row.get("notes", ""),
            ])
        if values:
            worksheet.append_rows(values, value_input_option="USER_ENTERED")
        return True, f"Saved {len(values)} opportunity/opportunities to Google Sheets."
    except Exception as exc:
        return False, f"Google Sheets export failed: {exc}"

# -----------------------------
# Session state
# -----------------------------
if "tracker" not in st.session_state:
    st.session_state.tracker = []
if "research_result" not in st.session_state:
    st.session_state.research_result = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""
if "resume_result" not in st.session_state:
    st.session_state.resume_result = ""
if "agent_result" not in st.session_state:
    st.session_state.agent_result = ""

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🧭 CareerCompass")
    st.caption("Your AI-assisted career research workspace")
    st.divider()

    st.subheader("Your career profile")
    student_name = st.text_input("Name (optional)", placeholder="Your name")
    major = st.text_input("Major / field of study", value="Computer Information Systems")
    location = st.text_input("Preferred location", value="Fresno, CA or Remote")
    desired_type = st.selectbox("Opportunity type", ["Any", "Internship", "Entry-level"])
    skills = st.text_area(
        "Skills and strengths",
        value="Excel, communication, customer service, problem solving, business processes",
        help="Separate skills with commas.",
        height=105,
    )
    experience = st.text_area(
        "Experience, projects, or coursework",
        placeholder="Example: coursework in information systems, customer service experience, class projects...",
        height=90,
    )

    st.divider()
    st.subheader("AI settings")
    api_key = st.text_input(
        "OpenAI API key (optional)",
        type="password",
        value=st.session_state.get("openai_api_key", ""),
        help="Used only during this app session. API billing is separate from ChatGPT.",
    )
    st.session_state.openai_api_key = api_key
    st.session_state.model_name = st.text_input(
        "Model",
        value=st.session_state.get("model_name", "gpt-4.1-mini"),
        help="You can change this to a model available to your API account.",
    )
    if api_key:
        st.success("API key entered for this session.")
    else:
        st.info("Demo mode: no API key required.")

profile = {
    "name": student_name,
    "major": major,
    "location": location,
    "desired_type": desired_type,
    "skills": skills,
    "experience": experience,
}

# -----------------------------
# Main header and navigation
# -----------------------------
st.title("CareerCompass")
st.write("Research opportunities, understand your fit, and organize your next career steps.")
st.caption("Starter build • Demo listings are fictional examples, not live vacancies.")

overview = st.columns(4)
overview[0].metric("Saved opportunities", len(st.session_state.tracker))
overview[1].metric("Career field", "CIS")
overview[2].metric("AI mode", "Live" if get_api_key() else "Demo")
overview[3].metric("Workspace", "Ready")

tabs = st.tabs([
    "🔎 Discover",
    "🧠 Analyze a Job",
    "📋 Application Tracker",
    "✍️ Resume Assistant",
    "ℹ️ About & Setup",
    "🤖 Career Agent",
])

# -----------------------------
# Discover
# -----------------------------
with tabs[0]:
    st.header("Discover opportunities")
    st.write("Start with illustrative sample listings, or ask the AI agent to research current opportunities online.")
    left, right = st.columns([1, 1])
    with left:
        if st.button("Load sample opportunities", width="stretch"):
            st.session_state.discovered_jobs = DEMO_JOBS.copy()
            st.success("Loaded three illustrative sample listings.")
    with right:
        if st.button("Research live opportunities with AI", type="primary", width="stretch"):
            if not get_api_key():
                st.warning("Enter your OpenAI API key in the sidebar to use live AI research. You can still explore the sample listings.")
            else:
                prompt = f"""
You are CareerPilot AI, a careful career research assistant.
Research current internship and entry-level opportunities using web search.
Candidate profile:
- Field of study: {profile['major']}
- Preferred location: {profile['location']}
- Opportunity type: {profile['desired_type']}
- Skills: {profile['skills']}
- Experience/coursework: {profile['experience']}

Find up to 5 relevant opportunities. Prioritize official employer career pages or reputable job boards.
For each opportunity provide: employer, exact job title, location/work mode, internship or entry-level status,
key requirements, why it may fit this candidate, and the direct source URL.
Do not invent openings, salary figures, deadlines, or URLs. If you cannot verify a detail, say so.
Include the date researched and clearly distinguish verified facts from your assessment.
"""
                with st.spinner("Researching current opportunities..."):
                    result, error = ai_response(prompt, use_web_search=True)
                if error:
                    st.error(error)
                else:
                    st.session_state.research_result = result or ""
                    st.success("Research completed. Review the sources and verify each listing before applying.")

    jobs = st.session_state.get("discovered_jobs", DEMO_JOBS)
    for index, job in enumerate(jobs):
        score, matched, missing = calculate_match(profile, job)
        with st.container(border=True):
            top = st.columns([3, 1])
            top[0].subheader(job["title"])
            top[1].metric("Baseline match", f"{score}%")
            st.write(f"**{job['company']}** • {job['location']} • {job['type']}")
            st.write(job["description"])
            if matched:
                st.caption("Matching skills: " + ", ".join(matched))
            if missing:
                st.caption("Skills not found in listing text: " + ", ".join(missing))
            st.caption("This score is a simple keyword-based estimate, not a hiring prediction.")
            actions = st.columns([1, 1, 3])
            if actions[0].button("Save to tracker", key=f"save_{index}_{job['title']}"):
                saved = dict(job)
                saved["match_score"] = score
                saved["status"] = "Interested"
                saved["date_added"] = datetime.now().strftime("%Y-%m-%d")
                saved["notes"] = ""
                if not any(x.get("title") == saved["title"] and x.get("company") == saved["company"] for x in st.session_state.tracker):
                    st.session_state.tracker.append(saved)
                    st.success("Saved to your tracker.")
                else:
                    st.info("This opportunity is already in your tracker.")
            actions[1].button("Review details", key=f"details_{index}_{job['title']}", help="Use the Analyze a Job tab to get a detailed AI review.")
            actions[2].markdown(f"[Open listing/source]({job['url']})")

    if st.session_state.research_result:
        st.divider()
        st.subheader("AI research report")
        st.markdown(st.session_state.research_result)
        st.download_button(
            "Download research report",
            data=st.session_state.research_result,
            file_name="careerpilot_research_report.md",
            mime="text/markdown",
        )

# -----------------------------
# Analyze a job
# -----------------------------
with tabs[1]:
    st.header("Analyze a job description")
    st.write("Paste a job posting to receive a match assessment and practical next steps.")
    job_title = st.text_input("Job title", placeholder="Example: IT Support Intern")
    company = st.text_input("Company", placeholder="Employer name")
    job_url = st.text_input("Job posting URL (optional)")
    job_description = st.text_area("Job description", height=230, placeholder="Paste the responsibilities and qualifications here...")
    if st.button("Analyze this opportunity", type="primary"):
        if not job_description.strip():
            st.warning("Paste a job description first.")
        else:
            job = {
                "title": job_title or "Untitled opportunity",
                "company": company or "Employer not specified",
                "description": job_description,
                "skills": "",
                "location": profile["location"],
                "work_mode": "",
                "type": profile["desired_type"],
            }
            score, matched, missing = calculate_match(profile, job)
            baseline = (
                f"### Initial keyword match: {score}%\n\n"
                f"**Skills found:** {', '.join(matched) if matched else 'No profile skills found in the pasted text.'}\n\n"
                f"**Skills not found:** {', '.join(missing) if missing else 'None'}\n\n"
                "This is a simple text-overlap estimate, not a hiring prediction."
            )
            prompt = f"""
Act as a practical career coach. Analyze this opportunity for the candidate below.
Candidate major: {profile['major']}
Candidate skills: {profile['skills']}
Candidate experience/coursework: {profile['experience']}
Candidate preferences: {profile['location']}; {profile['desired_type']}

Job title: {job_title}
Company: {company}
Job description:
{job_description}

Return:
1. A plain-language fit assessment.
2. Strongest matching qualifications.
3. Gaps or requirements the candidate should investigate.
4. Three honest resume bullet ideas based only on the candidate's supplied experience; do not invent accomplishments.
5. Five questions the candidate could ask the recruiter.
6. A clear recommendation: strong fit, possible fit, or weak fit, with reasoning.
Do not claim to know whether the employer will interview or hire the candidate.
"""
            result, error = ai_response(prompt)
            st.session_state.analysis_result = baseline + ("\n\n---\n\n" + result if result else "")
            if error:
                st.info(error)
            st.markdown(st.session_state.analysis_result)

    if st.session_state.analysis_result:
        st.download_button(
            "Download job analysis",
            data=st.session_state.analysis_result,
            file_name="careerpilot_job_analysis.md",
            mime="text/markdown",
        )

# -----------------------------
# Tracker
# -----------------------------
with tabs[2]:
    st.header("Application tracker")
    st.write("Keep track of opportunities you want to pursue.")
    if st.session_state.tracker:
        tracker_df = pd.DataFrame(st.session_state.tracker)
        display_cols = [c for c in ["company", "title", "location", "type", "match_score", "status", "url"] if c in tracker_df.columns]
        st.dataframe(tracker_df[display_cols], width="stretch", hide_index=True)
        csv = tracker_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download tracker as CSV", data=csv, file_name="careerpilot_tracker.csv", mime="text/csv")
        st.subheader("Update application status")
        options = [f"{i+1}. {item.get('title','Opportunity')} — {item.get('company','')}" for i, item in enumerate(st.session_state.tracker)]
        selected = st.selectbox("Choose an opportunity", options)
        selected_index = options.index(selected)
        new_status = st.selectbox("New status", ["Interested", "Preparing application", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"])
        notes = st.text_input("Notes (optional)", value=st.session_state.tracker[selected_index].get("notes", ""))
        if st.button("Update tracker entry"):
            st.session_state.tracker[selected_index]["status"] = new_status
            st.session_state.tracker[selected_index]["notes"] = notes
            st.success("Tracker updated.")
            st.rerun()
    else:
        st.info("No opportunities saved yet. Go to Discover and select Save to tracker.")

    st.divider()
    st.subheader("Optional: connect Google Sheets")
    st.write("This integration uses a Google service-account credentials file. Do not upload credentials to GitHub or share them publicly.")
    sheet_id = st.text_input("Google Spreadsheet ID", help="Copy the ID from the spreadsheet URL between /d/ and /edit.")
    credentials_path = st.text_input("Service-account JSON file path", value="google_service_account.json")
    if st.button("Save tracker to Google Sheets"):
        if not st.session_state.tracker:
            st.warning("Save at least one opportunity first.")
        elif not sheet_id.strip():
            st.warning("Enter your Google Spreadsheet ID.")
        elif not Path(credentials_path).exists():
            st.warning(f"Credentials file not found at: {credentials_path}")
        else:
            ok, message = save_to_google_sheets(st.session_state.tracker, sheet_id.strip(), credentials_path.strip())
            if ok:
                st.success(message)
            else:
                st.error(message)

# -----------------------------
# Resume assistant
# -----------------------------
with tabs[3]:
    st.header("Resume and cover letter assistant")
    st.write("Generate a first draft based on information you provide. Review every statement for accuracy.")
    resume_text = st.text_area(
        "Paste your current resume or relevant experience",
        value=profile["experience"],
        height=180,
        placeholder="Paste your resume, work history, projects, and coursework...",
    )
    target_job = st.text_area("Target job description", height=150, placeholder="Paste the job description...")
    document_type = st.radio("What would you like to draft?", ["Resume bullet improvements", "Cover letter"], horizontal=True)
    if st.button("Generate draft", type="primary"):
        if not resume_text.strip() or not target_job.strip():
            st.warning("Provide both your experience and the target job description.")
        else:
            prompt = f"""
You are a truthful career-writing assistant.
Create: {document_type}
Candidate's major: {profile['major']}
Candidate's skills: {profile['skills']}
Candidate's supplied experience/resume:
{resume_text}
Target job:
{target_job}

Tailor the writing to the target role. Never invent employers, dates, degrees, metrics, certifications,
technical skills, or achievements. Use clear professional language and mark any missing facts with
[ADD DETAIL] rather than guessing. Explain briefly what the candidate should verify before using the draft.
"""
            with st.spinner("Preparing your draft..."):
                result, error = ai_response(prompt)
            if error:
                st.error(error)
            else:
                st.session_state.resume_result = result or ""
                st.markdown(st.session_state.resume_result)
    if st.session_state.resume_result:
        st.download_button(
            "Download draft",
            data=st.session_state.resume_result,
            file_name="careerpilot_resume_draft.md",
            mime="text/markdown",
        )

# -----------------------------
# About and setup
# -----------------------------
with tabs[4]:
    st.header("About CareerPilot AI")
    st.write(
        "CareerPilot AI is a student-built career research assistant prototype. "
        "It combines a profile, opportunity research, transparent baseline matching, "
        "AI-assisted analysis, application tracking, and optional Google Sheets export."
    )
    st.subheader("What is automated?")
    st.markdown(
        "- **If/else logic:** checks whether required information or API credentials are present before actions.\n"
        "- **Loops:** iterates through opportunity listings, profile skills, and tracker records.\n"
        "- **AI agent workflow:** sends a goal and context to an AI model; live research can use web search.\n"
        "- **External application integration:** can append tracker entries to a Google Sheet when configured."
    )
    st.subheader("Important limitations")
    st.markdown(
        "- Sample listings are fictional training examples and must not be treated as real vacancies.\n"
        "- Live research results should be checked on the employer's official career page before applying.\n"
        "- Match scores are simple keyword-based estimates, not hiring probabilities.\n"
        "- AI-generated resume content must be reviewed and corrected by the user.\n"
        "- The app does not apply to jobs or send messages without the user's separate action."
    )
    st.subheader("Development notes")
    st.write("Record your prompts, decisions, bugs, fixes, and lessons learned in the included DEVELOPMENT_LOG.md.")
    st.caption("CareerPilot AI • Student project prototype")

# -----------------------------
# Advanced career agent
# -----------------------------
with tabs[5]:
    st.header("CareerPilot AI agent")
    st.write(
        "Run a guided, multi-step career workflow: research current openings, compare them "
        "with your profile, and create a practical action plan."
    )
    search_focus = st.text_input(
        "Research focus",
        value="CIS internships, IT support, business systems, data analysis, and help desk roles",
        help="Add role titles, industries, or skills you want the agent to prioritize.",
    )
    if st.button("Run the Career Agent", type="primary", width="stretch"):
        if not get_api_key():
            st.warning("Enter your OpenAI API key in the sidebar to run the Career Agent.")
        else:
            research_prompt = f"""
You are CareerPilot AI, a careful career research agent.
Research current internship and entry-level openings using web search.
Candidate profile:
- Field of study: {profile['major']}
- Preferred location: {profile['location']}
- Opportunity type: {profile['desired_type']}
- Skills: {profile['skills']}
- Experience/coursework: {profile['experience']}
Research focus: {search_focus}

Find up to 5 relevant opportunities. Prioritize Fresno, California and remote roles.
Use official employer career pages first, then reputable job boards. For each result include
company, exact title, location/work arrangement, internship or entry-level status, key
requirements, pay only when explicitly listed, and a direct source URL. Include the date
researched. Do not invent openings, salary, deadlines, requirements, or URLs. Clearly label
anything that could not be independently verified.
"""
            with st.spinner("Step 1 of 2: researching current opportunities..."):
                research, research_error = ai_response(research_prompt, use_web_search=True)
            if research_error:
                st.error(research_error)
            elif research:
                analysis_prompt = f"""
You are the analysis and planning stage of CareerPilot AI. Use only the research report
and candidate information below. Do not add job openings or factual details that are not
in the research report.

Candidate profile:
- Major: {profile['major']}
- Preferred location: {profile['location']}
- Opportunity type: {profile['desired_type']}
- Skills: {profile['skills']}
- Experience/coursework: {profile['experience']}

Research report:
{research}

Create a concise decision report with:
1. A comparison table of the researched roles and their stated locations/types.
2. A ranked shortlist based on the candidate's supplied skills, experience, and preferences.
3. For each shortlisted role, explain matching qualifications and gaps to investigate.
4. Recommend the best next action for each role (verify, prepare application, or skip),
   explaining the reasoning.
5. A 3-step plan for the candidate's next week.
6. Five useful questions to ask a recruiter.

Do not present a match estimate as a hiring probability. Do not claim the candidate is
qualified for requirements not supported by their profile. Preserve source URLs from the
research report so the candidate can verify every opening.
"""
                with st.spinner("Step 2 of 2: comparing roles and building your action plan..."):
                    recommendations, analysis_error = ai_response(analysis_prompt)
                if analysis_error:
                    st.error(analysis_error)
                if recommendations:
                    researched_on = datetime.now().strftime("%B %d, %Y")
                    st.session_state.agent_result = (
                        f"# CareerPilot AI Career Plan\n\nResearch date: {researched_on}\n\n"
                        f"## Live opportunity research\n\n{research}\n\n"
                        f"---\n\n## Personalized comparison and action plan\n\n{recommendations}"
                    )
                    st.success("Career Agent workflow completed. Verify each opening before applying.")

    if st.session_state.agent_result:
        st.markdown(st.session_state.agent_result)
        st.download_button(
            "Download Career Agent report",
            data=st.session_state.agent_result,
            file_name="careerpilot_agent_report.md",
            mime="text/markdown",
            width="stretch",
        )
        st.caption(
            "The agent researches and advises; it does not submit applications or contact employers. "
            "Check that each posting is still open on the employer's official website."
        )

st.divider()
st.caption("CareerPilot AI is an educational prototype. Verify job details independently and protect personal information.")
