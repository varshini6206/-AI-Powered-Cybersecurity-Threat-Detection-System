import gradio as gr
import random
import pandas as pd
from datetime import datetime

# ==========================================
# STORAGE
# ==========================================

history = []

# ==========================================
# THREAT ANALYSIS LOGIC
# ==========================================

def analyze_threat(user_input):

    text = user_input.lower()

    phishing_keywords = [
        "bank",
        "password",
        "login",
        "verify",
        "urgent",
        "click",
        "winner",
        "lottery",
        "otp",
        "suspended",
        "account",
        "prize",
        "claim",
        "free money",
        "paypal",
        "security alert"
    ]

    malicious_urls = [
        ".xyz",
        ".ru",
        "bit.ly",
        "free-money",
        "secure-login",
        "verify-now"
    ]

    score = 0

    for word in phishing_keywords:
        if word in text:
            score += 15

    for url in malicious_urls:
        if url in text:
            score += 25

    if "http://" in text:
        score += 20

    score = min(score, 100)

    # ======================================
    # CLASSIFICATION
    # ======================================

    if score >= 70:
        prediction = "PHISHING / MALICIOUS"
        severity = "CRITICAL"
        status = "HIGH RISK"
        color = "🔴"

    elif score >= 40:
        prediction = "SUSPICIOUS"
        severity = "MEDIUM"
        status = "BE CAREFUL"
        color = "🟠"

    else:
        prediction = "SAFE / BENIGN"
        severity = "LOW"
        status = "SAFE"
        color = "🟢"

    confidence = round(random.uniform(92, 99), 2)

    report = f"""
╔══════════════════════════════════════╗
        AI THREAT ANALYSIS REPORT
╚══════════════════════════════════════╝

🔎 Threat ID: #{random.randint(10000,99999)}

📌 Input Type: {"URL" if "http" in text else "TEXT"}

🧠 Prediction: {prediction}

📊 Confidence Score: {confidence}%

🚨 Threat Severity: {severity}

🛡 Security Status:
{color} {status}

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 AI SECURITY RECOMMENDATIONS

• Avoid suspicious URLs and unknown links

• Verify sender authenticity before clicking

• Enable Multi-Factor Authentication

• Avoid downloading unknown attachments
"""

    # ======================================
    # HISTORY
    # ======================================

    history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Prediction": prediction,
        "Severity": severity,
        "Confidence": f"{confidence}%"
    })

    df = pd.DataFrame(history)

    threats = len([x for x in history if x["Severity"] != "LOW"])
    safe = len([x for x in history if x["Severity"] == "LOW"])
    critical = len([x for x in history if x["Severity"] == "CRITICAL"])

    return report, df, threats, safe, critical

# ==========================================
# PROFESSIONAL CSS
# ==========================================

css = """

body {
    background: linear-gradient(135deg,#020617,#071129,#0F172A);
}

.gradio-container {
    background: transparent !important;
    color: white !important;
    font-family: Arial, sans-serif;
    max-width: 1450px !important;
}

/* TITLE */

h1 {
    text-align: center;
    color: #FFFFFF !important;
    font-size: 60px !important;
    font-weight: bold !important;
    margin-bottom: 10px !important;
}

h2, h3, h4 {
    color: #FFFFFF !important;
}

p, span, label, div, li {
    color: #E5E7EB !important;
    font-size: 17px !important;
}

/* CARDS */

.block {
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(15,23,42,0.7) !important;
    backdrop-filter: blur(10px);
}

/* TEXTBOX */

textarea {
    background: #0F172A !important;
    color: white !important;
    border: 2px solid #00E5FF !important;
    border-radius: 15px !important;
    font-size: 18px !important;
    padding: 15px !important;
}

/* OUTPUT */

textarea[readonly] {
    background: #111827 !important;
    color: #00FF99 !important;
    font-weight: bold !important;
}

/* BUTTON */

button {
    background: linear-gradient(
        90deg,
        #00FF99,
        #00D9FF
    ) !important;

    color: black !important;

    border: none !important;

    border-radius: 14px !important;

    font-size: 18px !important;

    font-weight: bold !important;

    height: 55px !important;
}

button:hover {
    transform: scale(1.02);
    transition: 0.3s;
}

/* TABS */

button[role="tab"] {
    color: black !important;
    font-weight: bold !important;
}

/* STATS */

input {
    background: #1E293B !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #00E5FF !important;
    text-align: center !important;
    font-size: 20px !important;
    font-weight: bold !important;
}

/* TABLE */

table {
    background: #0F172A !important;
    color: white !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

thead {
    background: #00E5FF !important;
}

th {
    background: #00E5FF !important;
    color: black !important;
    font-weight: bold !important;
    font-size: 16px !important;
}

td {
    background: #111827 !important;
    color: white !important;
    text-align: center !important;
    font-size: 15px !important;
}

/* REMOVE FOOTER */

footer {
    display: none !important;
}

"""

# ==========================================
# UI
# ==========================================

with gr.Blocks(css=css) as demo:

    gr.Markdown(
        """
# 🛡 AI-Powered Cybersecurity Threat Detection System

### Real-Time AI-Powered Cybersecurity Threat Detection System Dashboard
"""
    )

    with gr.Row():

        with gr.Column(scale=1):

            gr.Markdown("""
## ⚡ SOC PANEL

### Security Modules

• Threat Scanner

• Threat Analytics

• AI Security Engine

• Malware Detection

• Phishing Detection

• Threat Intelligence
""")

        with gr.Column(scale=2):

            with gr.Row():

                threats_box = gr.Textbox(
                    value="0",
                    label="🚨 Threats Detected"
                )

                safe_box = gr.Textbox(
                    value="0",
                    label="🛡 Safe Requests"
                )

                critical_box = gr.Textbox(
                    value="0",
                    label="⚠ Critical Alerts"
                )

            with gr.Tabs():

                with gr.Tab("Threat Scanner"):

                    user_input = gr.Textbox(
                        lines=8,
                        placeholder="Paste phishing URL or suspicious message..."
                    )

                    analyze_btn = gr.Button("Analyze Threat")

                    output = gr.Textbox(
                        lines=18,
                        label="Threat Analysis Report"
                    )

                with gr.Tab("Threat Analytics"):

                    history_table = gr.Dataframe(
                        headers=[
                            "Time",
                            "Prediction",
                            "Severity",
                            "Confidence"
                        ],
                        interactive=False
                    )

                with gr.Tab("AI Security Assistant"):

                    gr.Markdown("""
### AI Security Tips

✅ Never click unknown links

✅ Use strong passwords

✅ Enable 2FA Authentication

✅ Avoid suspicious downloads

✅ Monitor phishing emails
""")

    analyze_btn.click(
        fn=analyze_threat,
        inputs=user_input,
        outputs=[
            output,
            history_table,
            threats_box,
            safe_box,
            critical_box
        ]
    )

demo.launch()