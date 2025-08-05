import streamlit as st
import json
import google.generativeai as genai
import smtplib, ssl
from email.message import EmailMessage
import re
from datetime import datetime

# --- Setup ---
st.set_page_config(page_title="AlertAid Hazard Classifier", layout="centered")
st.markdown("""
<style>
/* Custom Font & Scrollbar */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

html, body, .main, .stApp {
    font-family: 'Inter', sans-serif;
    color: #f1f1f1;
    scroll-behavior: smooth;
}

/* Title & Header Styling */
h1, h2, .stTitle {
    font-weight: 600;
    color: #facc15 !important;
}

/* Input area */
textarea, input {
    background-color: #1f2937 !important;
    color: #f9fafb !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
}

/* Buttons */
button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    transition: 0.3s ease-in-out;
}
button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
    transform: scale(1.05);
}

/* Highlight badge */
.highlight {
    background: linear-gradient(90deg, #fde68a, #fcd34d);
    color: #1e293b;
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 600;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

/* Report Box */
.report-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    margin-top: 25px;
    transition: 0.3s ease;
}
.report-box:hover {
    transform: translateY(-4px);
}

/* Code Output Area */
.report-box pre {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: #e0f2fe;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 0;
}

/* Spinner customization */
.css-1v0mbdj {
    color: #facc15 !important;
}

/* Download button */
.css-1offfwp {
    background-color: #22c55e !important;
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
}
.css-1offfwp:hover {
    background-color: #16a34a !important;
}
</style>
""", unsafe_allow_html=True)


st.title("🚨 AlertAid")
st.subheader("AI-powered Workplace Hazard Analyzer")

# Initialize session state to store result after classification
if "hazard_result" not in st.session_state:
    st.session_state.hazard_result = None

api_key = st.secrets["GOOGLE_API_KEY"]
user_input = st.text_area("📝 Describe the Hazard", height=150, placeholder="e.g., Oil spill near machine, no signage, workers slipping...")

def classify_hazard(text):
    prompt = f"""
You are a certified workplace safety AI. Analyze the given hazard description and classify its severity. Then generate a structured safety report in the exact format below.

Return a JSON with:
- hazard_level (High, Medium, Low)
- severity (1, 2, 3)
- report_text: structured like this 👇

---

Safety Incident Report

Date: [today's date]  
Time: [current time]  
Location: [infer from input, else say "Not specified"]

Description: [summary of hazard]  
Injuries Reported: [if any, else "None"]  
Witnesses: [if mentioned, else "Not mentioned"]  
Actions Taken: [what should be or was done]  
Recommendations: [how to prevent recurrence]

---

Now analyze this:

Input: '{text}'

Respond ONLY with the JSON object.

"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    match = re.search(r"\{.*\}", response.text, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        st.error("❌ Could not parse Gemini's JSON output.")
        return None

def send_email_streamlit(subject, body, recipient_email, sender_email, app_password):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False

if st.button("🚀 Analyze Hazard") and api_key and user_input:
    try:
        genai.configure(api_key=api_key)
        with st.spinner("🧠 Thinking like a safety officer..."):
            result = classify_hazard(user_input)
        st.session_state.hazard_result = result  # ✅ Save the result
    except Exception as e:
        st.error(f"❌ Error: {e}")

result = st.session_state.hazard_result  # ✅ Retrieve from session

if result:
    severity = int(result['severity'])
    st.markdown(f"**Hazard Level:** <span class='highlight'>{result['hazard_level']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Severity:** <span class='highlight'>{result['severity']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='report-box'><pre>{result['report_text']}</pre></div>", unsafe_allow_html=True)

    if severity == 1:
        st.warning("⚠️ High Risk Detected! Please send report to your email.")
        sender_email = st.text_input("Enter your Gmail address:", key="email_input")
        app_password = st.text_input("Enter your 16-digit Gmail App Password:", type="password", key="password_input")
        if st.button("📨 Send Email"):
            subject = "🚨 High-Risk Workplace Hazard Alert"
            body = result["report_text"]
            
            sent_to = "nityachintan13@gmail.com"
            
            if send_email_streamlit(subject, body, sent_to, sender_email, app_password):
                st.success("✅ Email sent successfully!")

    elif severity == 2:
        st.info("📝 Medium risk logged.")
        with open("medium_risk_log.txt", "a") as log:
            log.write(f"\n==== MEDIUM RISK ===={datetime.now()}\n{result['report_text']}\n")

    else:
        st.success("✅ Low risk. No action needed.")
        if "Recommendations:" in result['report_text']:
            st.markdown("**Gemini's Recommendation:**")
            st.info(result['report_text'].split("Recommendations:")[-1].strip())
            
import os

# Show download button if the file exists
if os.path.exists("medium_risk_log.txt"):
    with open("medium_risk_log.txt", "r") as file:
        log_data = file.read()
    st.download_button(
        label="⬇️ Download Medium Risk Log",
        data=log_data,
        file_name="medium_risk_log.txt",
        mime="text/plain"
    )
else:
    st.info("🗂 No medium risk log file available yet.")
