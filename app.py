import subprocess
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RasmalAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOGO PATH
# =========================================================

logo_path = r"C:\Users\utkra\Downloads\WhatsApp Image 2026-05-25 at 12.36.03 AM.jpeg"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #080808;
    color: white;
}

/* ----------------------------------------------------- */
/* MAIN */
/* ----------------------------------------------------- */

[data-testid="stAppViewContainer"] {
    background-color: #080808;
}

[data-testid="stHeader"] {
    background-color: #080808;
    height: 0px;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    background-color: #080808;
}

.main {
    background-color: #080808 !important;
}

/* ----------------------------------------------------- */
/* SIDEBAR */
/* ----------------------------------------------------- */

section[data-testid="stSidebar"] {
    background-color: #0B0B0B;
    border-right: 1px solid #1E1E1E;
}

section[data-testid="stSidebar"] img {
    border-radius: 16px;
}

/* ----------------------------------------------------- */
/* CARD */
/* ----------------------------------------------------- */

.rasmal-card {
    background-color: #101010;
    border: 1px solid #232323;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
}

/* ----------------------------------------------------- */
/* TITLES */
/* ----------------------------------------------------- */

.section-title {
    color: #D6A84A;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.6px;
    margin-bottom: 14px;
}

/* ----------------------------------------------------- */
/* BUTTONS */
/* ----------------------------------------------------- */

div.stButton > button {
    background-color: #C89B3C;
    color: black;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.7rem 1rem;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #E6B85C;
}

/* ----------------------------------------------------- */
/* INPUT */
/* ----------------------------------------------------- */

.stTextInput input {
    background-color: #101010;
    color: white;
    border: 1px solid #2E2E2E;
    border-radius: 10px;
}

/* ----------------------------------------------------- */
/* LOG BOX */
/* ----------------------------------------------------- */

.log-box {
    background-color: #0C0C0C;
    border: 1px solid #232323;
    border-radius: 16px;
    padding: 18px;
    min-height: 420px;
    font-family: monospace;
}

/* ----------------------------------------------------- */
/* EXECUTIVE SUMMARY */
/* ----------------------------------------------------- */

.summary-card {
    background-color: #101010;
    border-radius: 16px;
    padding: 24px;
    border-left: 6px solid #D6A84A;
    border: 1px solid #232323;
    margin-top: 10px;
}

.summary-critical {
    border-left: 6px solid #ff4b4b;
}

.summary-high {
    border-left: 6px solid #ff944d;
}

.summary-elevated {
    border-left: 6px solid #D6A84A;
}

.summary-nominal {
    border-left: 6px solid #4CAF50;
}

.summary-title {
    font-size: 13px;
    color: #999;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 10px;
}

.summary-value {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 14px;
}

.summary-text {
    color: #DDD;
    line-height: 1.7;
    font-size: 15px;
}

.action-card {
    background-color: #151515;
    border: 1px solid #262626;
    border-radius: 12px;
    padding: 14px;
    margin-top: 12px;
}

.priority-tag {
    color: #D6A84A;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

/* ----------------------------------------------------- */
/* PULSE */
/* ----------------------------------------------------- */

.pulse-green {
    color: #4CAF50;
    animation: pulse 1.5s infinite;
}

.pulse-red {
    color: #ff4b4b;
    animation: pulse 1.2s infinite;
}

.pulse-gold {
    color: #D6A84A;
    animation: pulse 1.7s infinite;
}

@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1; }
    100% { opacity: 0.4; }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CORAL QUERY
# =========================================================

def run_coral_query(query):

    result = subprocess.run(
        ["coral", "sql", query],
        capture_output=True,
        text=True
    )

    if result.stderr:
        return f"ERROR:\n{result.stderr}"

    return result.stdout

# =========================================================
# AI LOGS
# =========================================================

def generate_dynamic_logs(data):

    logs = []

    timestamp = datetime.now().strftime("%H:%M:%S")

    keyword_map = {
        "authentication": (
            "Authentication anomaly detected",
            "warning"
        ),
        "rollback": (
            "Rollback sequence correlated",
            "warning"
        ),
        "critical": (
            "Critical advisory escalation triggered",
            "critical"
        ),
        "breach": (
            "Potential security breach identified",
            "critical"
        ),
        "exploit": (
            "Exploit intelligence feed updated",
            "critical"
        ),
        "failure": (
            "Repeated operational failures detected",
            "warning"
        ),
        "incident": (
            "Incident correlation score increased",
            "warning"
        ),
        "unauthorized": (
            "Unauthorized access pattern detected",
            "critical"
        )
    }

    lowered = data.lower()

    for key, value in keyword_map.items():

        if key in lowered:

            logs.append({
                "time": timestamp,
                "message": value[0],
                "severity": value[1]
            })

    logs.append({
        "time": timestamp,
        "message": "Live intelligence synchronization active",
        "severity": "normal"
    })

    logs.append({
        "time": timestamp,
        "message": "AI correlation engine operational",
        "severity": "normal"
    })

    return logs

# =========================================================
# RISK CALCULATION
# =========================================================

def calculate_risk_score(
    incident_mentions,
    critical_count,
    high_count
):

    score = (
        incident_mentions * 15
        + critical_count * 25
        + high_count * 12
    )

    return min(score, 100)

# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([6, 2])

with header_left:

    logo_col, text_col = st.columns([1, 5])

    with logo_col:

        st.image(
            logo_path,
            width=90
        )

    with text_col:

        st.markdown("""
        <div style="padding-top:10px;">

        <div style="
            font-size:54px;
            font-weight:800;
            color:#E6C07B;
            line-height:1;
        ">
        RasmalAI
        </div>

        <div style="
            color:#F2F2F2;
            font-size:24px;
            margin-top:12px;
            font-weight:500;
        ">
        AI-Powered Security Intelligence Command Center
        </div>

        <div style="
            color:#777;
            margin-top:8px;
            font-size:13px;
            letter-spacing:1px;
        ">
        PREMIUM INCIDENT CORRELATION & THREAT INTELLIGENCE PLATFORM
        </div>

        </div>
        """, unsafe_allow_html=True)

with header_right:

    current_time = datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
    <div style="
        background-color:#101010;
        border:1px solid #232323;
        border-radius:16px;
        padding:20px;
        text-align:center;
        margin-top:12px;
    ">

    <div style="
        color:#4CAF50;
        font-size:13px;
        font-weight:700;
        margin-bottom:10px;
    ">
    ● NODE_ACTIVE
    </div>

    <div style="
        color:#E6C07B;
        font-size:38px;
        font-weight:800;
    ">
    {current_time}
    </div>

    <div style="
        color:#777;
        font-size:12px;
        margin-top:6px;
    ">
    LIVE INTELLIGENCE SESSION
    </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        logo_path,
        width=180
    )

    st.markdown("<br>", unsafe_allow_html=True)

    main_mode = st.radio(
        "INTELLIGENCE MODES",
        [
            "GitHub Intelligence",
            "Slack Intelligence",
            "Incident Correlation"
        ]
    )

# =========================================================
# CHANNELS
# =========================================================

slack_channels = {
    "prod-incidents": "C0B5LPBQSDR",
    "security-alerts": "C0B5WNUL6A0",
    "backend-team": "C0B5V016BT3"
}

query_data = ""

# =========================================================
# GITHUB
# =========================================================

if main_mode == "GitHub Intelligence":

    with st.sidebar:

        github_mode = st.radio(
            "GITHUB SUBSYSTEM",
            [
                "Security Advisories",
                "Threat Feed",
                "Repository Monitoring"
            ]
        )

    # -----------------------------------------------------
    # SECURITY ADVISORIES
    # -----------------------------------------------------

    if github_mode == "Security Advisories":

        query = """
        SELECT
            ghsa_id,
            summary,
            severity
        FROM github.advisories
        LIMIT 8
        """

        query_data = run_coral_query(query)

    # -----------------------------------------------------
    # THREAT FEED
    # -----------------------------------------------------

    elif github_mode == "Threat Feed":

        query = """
        SELECT
            ghsa_id,
            summary,
            severity
        FROM github.advisories
        LIMIT 20
        """

        raw_query_data = run_coral_query(query)

        filtered_lines = []

        for line in raw_query_data.splitlines():

            lowered = line.lower()

            if (
                "critical" in lowered
                or "high" in lowered
            ):
                filtered_lines.append(line)

        if filtered_lines:

            query_data = "\n".join(filtered_lines)

        else:

            query_data = raw_query_data

    # -----------------------------------------------------
    # REPOSITORY MONITORING
    # -----------------------------------------------------

    else:

        query = """
        SELECT
            title,
            state,
            repository__full_name,
            html_url
        FROM github.issues
        LIMIT 10
        """

        # query_data = run_coral_query(query)

    

# =========================================================
# SLACK
# =========================================================

elif main_mode == "Slack Intelligence":

    with st.sidebar:

        selected_channel = st.radio(
            "SLACK FEEDS",
            list(slack_channels.keys())
        )

    channel_id = slack_channels[selected_channel]

    query = f"""
    SELECT
        ts,
        user_id,
        text
    FROM slack.messages(
        channel => '{channel_id}'
    )
    ORDER BY ts DESC
    LIMIT 12
    """

    query_data = run_coral_query(query)

# =========================================================
# CORRELATION
# =========================================================

else:

    github_query = """
    SELECT
        ghsa_id,
        summary,
        severity
    FROM github.advisories
    LIMIT 6
    """

    repo_query = """
    SELECT
        title,
        state,
        repository__full_name,
        html_url
    FROM github.issues
    LIMIT 5
    """

    slack_query = """
    SELECT
        ts,
        user_id,
        text
    FROM slack.messages(
        channel => 'C0B5WNUL6A0'
    )
    ORDER BY ts DESC
    LIMIT 10
    """

    github_results = run_coral_query(github_query)
    repo_results = run_coral_query(repo_query)
    slack_results = run_coral_query(slack_query)

    query_data = f"""
SECURITY ADVISORIES
{github_results}

REPOSITORY MONITORING
{repo_results}

SLACK INCIDENT FEED
{slack_results}
"""

# =========================================================
# ANALYSIS
# =========================================================

incident_keywords = [
    "critical",
    "error",
    "failure",
    "incident",
    "rollback",
    "authentication",
    "unauthorized",
    "breach",
    "exploit",
    "latency",
    "attack",
    "outage"
]

incident_mentions = 0

for keyword in incident_keywords:
    incident_mentions += query_data.lower().count(keyword)

critical_count = query_data.lower().count("critical")
high_count = query_data.lower().count("high")

risk_score = calculate_risk_score(
    incident_mentions,
    critical_count,
    high_count
)

correlation_confidence = min(
    55 + incident_mentions * 4,
    97
)

active_signals = (
    incident_mentions
    + critical_count
    + high_count
)

# =========================================================
# RISK LEVEL
# =========================================================

if risk_score >= 80:

    risk_level = "CRITICAL"
    risk_color = "#ff4b4b"

elif risk_score >= 45:

    risk_level = "HIGH"
    risk_color = "#ff944d"

elif risk_score >= 25:

    risk_level = "ELEVATED"
    risk_color = "#D6A84A"

else:

    risk_level = "NOMINAL"
    risk_color = "#4CAF50"

# =========================================================
# METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(f"""
    <div class="rasmal-card">

    <div class="section-title">
    RISK INDEX
    </div>

    <div style="
        font-size:46px;
        font-weight:800;
        color:{risk_color};
    ">
    {risk_level}
    </div>

    </div>
    """, unsafe_allow_html=True)

with m2:

    st.markdown(f"""
    <div class="rasmal-card">

    <div class="section-title">
    CORRELATION CONFIDENCE
    </div>

    <div style="
        font-size:46px;
        font-weight:800;
        color:#E6C07B;
    ">
    {correlation_confidence}%
    </div>

    </div>
    """, unsafe_allow_html=True)

with m3:

    st.markdown(f"""
    <div class="rasmal-card">

    <div class="section-title">
    ACTIVE SIGNALS
    </div>

    <div style="
        font-size:46px;
        font-weight:800;
        color:#D6A84A;
    ">
    {active_signals}
    </div>

    </div>
    """, unsafe_allow_html=True)

with m4:

    system_status = (
        "OBSERVING"
        if risk_level in ["CRITICAL", "HIGH"]
        else "STABLE"
    )

    status_color = (
        "#ff944d"
        if system_status == "OBSERVING"
        else "#4CAF50"
    )

    st.markdown(f"""
    <div class="rasmal-card">

    <div class="section-title">
    SYSTEM STATUS
    </div>

    <div style="
        font-size:40px;
        font-weight:800;
        color:{status_color};
    ">
    {system_status}
    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TIMELINE
# =========================================================

st.markdown("""
<div class="section-title">
AI CORRELATION TIMELINE
</div>
""", unsafe_allow_html=True)

dynamic_logs = generate_dynamic_logs(query_data)

log_html = ""

for log in dynamic_logs:

    if log["severity"] == "critical":
        color = "#ff4b4b"

    elif log["severity"] == "warning":
        color = "#ff944d"

    else:
        color = "#D6A84A"

    log_html += f"""
    <div style='margin-bottom:16px;'>

    <span style='color:#666'>
    [{log["time"]}]
    </span>

    <span style='color:{color}; font-weight:700'>
    {log["message"]}
    </span>

    </div>
    """

st.markdown(
    f"""
    <div class="log-box">
    {log_html}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# RAW DATA
# =========================================================

with st.expander("View Intelligence Data"):

    st.code(query_data, language="text")

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

enable_summary = st.toggle(
    "Enable Executive Intelligence Summary",
    value=False
)

if enable_summary:

    st.markdown("""
    <div class="section-title">
    EXECUTIVE INTELLIGENCE SUMMARY
    </div>
    """, unsafe_allow_html=True)

    prompt = f"""
    You are RasmalAI,
    an elite cyber intelligence platform.

    Operational Intelligence:
    {query_data}

    Risk Level:
    {risk_level}

    Correlation Confidence:
    {correlation_confidence}

    Return ONLY in this exact structure:

    THREAT_LEVEL:
    (one word)

    PRIMARY_CONCERN:
    (1 concise sentence)

    IMPACT:
    (1 concise operational impact sentence)

    IMMEDIATE_ACTIONS:
    - short bullet
    - short bullet
    - short bullet

    Keep concise.
    Tactical.
    Enterprise-grade.
    No markdown formatting.
    """

    try:

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        summary = (
            completion
            .choices[0]
            .message
            .content
        )

        summary = summary.replace("**", "")

        lines = summary.splitlines()

        threat_level = ""
        primary_concern = ""
        impact = ""
        actions = []

        for line in lines:

            line = line.strip()

            if line.startswith("THREAT_LEVEL:"):

                threat_level = (
                    line.replace(
                        "THREAT_LEVEL:",
                        ""
                    ).strip()
                )

            elif line.startswith("PRIMARY_CONCERN:"):

                primary_concern = (
                    line.replace(
                        "PRIMARY_CONCERN:",
                        ""
                    ).strip()
                )

            elif line.startswith("IMPACT:"):

                impact = (
                    line.replace(
                        "IMPACT:",
                        ""
                    ).strip()
                )

            elif line.startswith("-"):

                actions.append(
                    line.replace("-", "").strip()
                )

        if "CRITICAL" in threat_level.upper():

            severity_class = "summary-critical"
            severity_color = "#ff4b4b"

        elif "HIGH" in threat_level.upper():

            severity_class = "summary-high"
            severity_color = "#ff944d"

        elif "ELEVATED" in threat_level.upper():

            severity_class = "summary-elevated"
            severity_color = "#D6A84A"

        else:

            severity_class = "summary-nominal"
            severity_color = "#4CAF50"

        st.markdown(f"""
        <div class="summary-card {severity_class}">

        <div class="summary-title">
        THREAT SEVERITY
        </div>

        <div class="summary-value"
        style="color:{severity_color};">
        {threat_level}
        </div>

        <div class="summary-title">
        PRIMARY CONCERN
        </div>

        <div class="summary-text">
        {primary_concern}
        </div>

        <br>

        <div class="summary-title">
        OPERATIONAL IMPACT
        </div>

        <div class="summary-text">
        {impact}
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-title">
        IMMEDIATE RESPONSE ACTIONS
        </div>
        """, unsafe_allow_html=True)

        for idx, action in enumerate(actions):

            st.markdown(f"""
            <div class="action-card">

            <div class="priority-tag">
            PRIORITY {idx + 1}
            </div>

            <div class="summary-text">
            {action}
            </div>

            </div>
            """, unsafe_allow_html=True)

    except Exception as e:

        st.error(f"Summary Error: {e}")

# =========================================================
# ANALYSIS ENGINE
# =========================================================

st.markdown("""
<div class="section-title">
RASMALAI ANALYSIS ENGINE
</div>
""", unsafe_allow_html=True)

user_input = st.text_input(
    "Ask RasmalAI about operational intelligence..."
)

if st.button("Run Intelligence Analysis"):

    if user_input.strip() == "":

        st.warning("Please enter a question.")

    else:

        prompt = f"""
        You are RasmalAI,
        an elite AI security intelligence platform.

        Operational Intelligence:
        {query_data}

        Risk Level:
        {risk_level}

        Correlation Confidence:
        {correlation_confidence}

        User Query:
        {user_input}

        Return:
        - Threat Severity
        - Correlated Findings
        - Risks
        - Recommended Actions

        Tactical and enterprise-focused.
        """

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        response = (
            completion
            .choices[0]
            .message
            .content
        )

        st.markdown("""
        <div class="section-title">
        ANALYSIS RESPONSE
        </div>
        """, unsafe_allow_html=True)

        if risk_level == "CRITICAL":

            st.error(response)

        elif risk_level in ["HIGH", "ELEVATED"]:

            st.warning(response)

        else:

            st.success(response)