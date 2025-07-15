
# 🚨 AlertAid: Workplace Hazard Classifier & Safety Reporter

AlertAid is a Streamlit-based web application that uses Google's Gemini AI (via `google-generativeai`) to classify workplace hazard descriptions by severity and generate structured safety reports. It can also log medium-risk incidents and email high-risk alerts to safety authorities.

---

🔗 **Live App:**  
[https://alertaid.streamlit.app/](https://alertaid.streamlit.app/)

---

## ✅ Features

- 🌐 Gemini 1.5 Flash integration for intelligent hazard classification
- 🧠 Natural language input (just describe the hazard)
- 📊 Severity-based decision logic:
  - High → Email alert to authority
  - Medium → Log to file
  - Low → Show recommendations only
- 📧 Secure Gmail-based email sending for high-risk cases
- 🔒 Streamlit Secrets used for secure API key handling

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/alertaid.git
cd alertaid
```

### 2. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add API Key to Streamlit Secrets

Create a `.streamlit/secrets.toml` file:

```
[general]
GOOGLE_API_KEY = "your-google-api-key"
```

**Never upload this file to GitHub.** It's already in `.gitignore`.

---

## 🧪 Running the App

```bash
streamlit run app.py
```

You can now open the web app in your browser and describe a workplace hazard!

---

## 📄 Logs

Medium-risk incidents are saved in:

```
medium_risk_log.txt
```

Use the **Download Log** button in the app to export it.

---

## 📧 Email Sending

For high-risk cases, you'll be prompted to enter:
- Gmail address (sender)
- 16-digit Gmail App Password (not your real password!)

Email will be sent to your configured recipient (you can change it in `app.py`).

---

## ✅ Requirements

- Python 3.8+
- Packages:
  - `streamlit`
  - `google-generativeai`
  - `python-dotenv` (optional for local `.env` usage)

---

## 📌 Notes

- Do **not** upload `.streamlit/secrets.toml` or `.env` to GitHub.
- You can deploy this app on **Streamlit Cloud** for free.

---

## 📘 License

MIT License. See `LICENSE` file for details.

---

## ✨ Made by

[@Nitya-Mehta](https://github.com/Nitya-Mehta)
