import subprocess
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Streamlit page config
st.set_page_config(
    page_title="RasmalAI",
    page_icon="🛡️",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }

    h1, h2, h3 {
        color: white;
    }

    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 12px;
    }

    .stCodeBlock {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Function to run Coral SQL queries
def run_coral_query(query):

    result = subprocess.run(
        ["coral", "sql", query],
        capture_output=True,
        text=True
    )

    return result.stdout

# ---------------- UI ---------------- #

st.title("🛡️ RasmalAI")
st.subheader("Enterprise Security Intelligence Agent")

# Intelligence Mode Selector
data_mode = st.selectbox(
    "Select Intelligence Mode",
    [
        "Security Advisories",
        "GitHub Issues",
        "Slack Intelligence",
        "Incident Correlation"
    ]
)

# ---------------- SLACK CHANNEL MAP ---------------- #

slack_channels = {
    "prod-incidents": "C0B5LPBQSDR",
    "security-alerts": "C0B5WNUL6A0",
    "backend-team": "C0B5V016BT3"
}

# ---------------- QUERY LOGIC ---------------- #

if data_mode == "Security Advisories":

    severity_filter = st.selectbox(
        "Select Severity Level",
        ["all", "critical", "high", "medium"]
    )

    if severity_filter == "all":

        query = """
        SELECT ghsa_id, summary, severity
        FROM github.advisories
        LIMIT 5
        """

    else:

        query = f"""
        SELECT ghsa_id, summary, severity
        FROM github.advisories
        WHERE severity = '{severity_filter}'
        LIMIT 5
        """

    query_data = run_coral_query(query)

elif data_mode == "GitHub Issues":

    query = """
    SELECT id, title, state
    FROM github.issues
    LIMIT 5
    """

    query_data = run_coral_query(query)

elif data_mode == "Slack Intelligence":
        


        selected_channel = st.selectbox(
        "Select Slack Channel",
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
        LIMIT 10
        """

        query_data = run_coral_query(query)

else:

    github_query = """
    SELECT id, title, state
    FROM github.issues
    LIMIT 5
    """

    slack_query = """
    SELECT id, name, is_archived
    FROM slack.channels
    LIMIT 5
    """

    github_results = run_coral_query(github_query)
    slack_results = run_coral_query(slack_query)

    query_data = f"""
GITHUB ISSUES:
{github_results}

SLACK CHANNELS:
{slack_results}
"""

# ---------------- METRICS ---------------- #

col1, col2, col3 = st.columns(3)

if data_mode == "Security Advisories":

    critical_count = query_data.lower().count("critical")
    high_count = query_data.lower().count("high")
    medium_count = query_data.lower().count("medium")

    col1.metric("Critical Findings", critical_count)
    col2.metric("High Findings", high_count)
    col3.metric("Medium Findings", medium_count)

elif data_mode == "GitHub Issues":

    open_count = query_data.lower().count("open")
    closed_count = query_data.lower().count("closed")

    col1.metric("Open Issues", open_count)
    col2.metric("Closed Issues", closed_count)
    col3.metric("Total Records", 5)

elif data_mode == "Slack Intelligence":

    archived_count = query_data.lower().count("true")
    active_count = query_data.lower().count("false")

    col1.metric("Archived Channels", archived_count)
    col2.metric("Active Channels", active_count)
    col3.metric("Total Channels", 5)

else:

    issue_count = query_data.lower().count("open")
    channel_count = query_data.lower().count("false")

    col1.metric("Operational Issues", issue_count)
    col2.metric("Active Channels", channel_count)
    col3.metric("Correlation Mode", "ON")

# ---------------- DATA DISPLAY ---------------- #

st.write(f"## {data_mode}")

st.code(query_data, language="text")

# ---------------- EXECUTIVE DASHBOARD ---------------- #

left_col, right_col = st.columns([1, 1])

# ---------------- LEFT SIDE ---------------- #

with left_col:

    st.write("## 📊 Intelligence Overview")

    if data_mode == "Security Advisories":

        chart_data = pd.DataFrame({
            "Category": ["Critical", "High", "Medium"],
            "Count": [
                query_data.lower().count("critical"),
                query_data.lower().count("high"),
                query_data.lower().count("medium")
            ]
        })

        chart_title = "Security Severity Distribution"

    elif data_mode == "GitHub Issues":

        chart_data = pd.DataFrame({
            "Category": ["Open", "Closed"],
            "Count": [
                query_data.lower().count("open"),
                query_data.lower().count("closed")
            ]
        })

        chart_title = "GitHub Issue Status"

    elif data_mode == "Slack Intelligence":

        chart_data = pd.DataFrame({
            "Category": ["Active Channels", "Archived Channels"],
            "Count": [
                query_data.lower().count("false"),
                query_data.lower().count("true")
            ]
        })

        chart_title = "Slack Workspace Status"

    else:

        chart_data = pd.DataFrame({
            "Category": ["Operational Issues", "Slack Channels"],
            "Count": [
                query_data.lower().count("open"),
                query_data.lower().count("false")
            ]
        })

        chart_title = "Incident Correlation Signals"

    fig = px.pie(
        chart_data,
        names="Category",
        values="Count",
        hole=0.55,
        title=chart_title
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        title_font_size=22,
        legend_font_size=14,
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- RIGHT SIDE ---------------- #

with right_col:

    enable_ai_summary = st.toggle(
        "Enable AI Executive Summary",
        value=False
    )

    if enable_ai_summary:

        st.write("## 🚨 Executive Summary")

        summary_prompt = f"""
        You are an enterprise observability analyst.

        Analyze the following intelligence data and provide
        a short executive summary for leadership.

        Intelligence Type:
        {data_mode}

        Data:
        {query_data}

        Return:
        - Overall Risk Level
        - Key Operational Concern
        - Recommended Immediate Action

        Keep it concise and professional.
        """

        try:

            summary_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": summary_prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )

            executive_summary = (
                summary_completion
                .choices[0]
                .message.content
            )

            st.info(executive_summary)

            # ---------------- RISK STATUS ---------------- #

            risk_text = executive_summary.upper()

            st.write("## 🚦 Risk Status")

            if "CRITICAL" in risk_text:

                st.error("🔴 CRITICAL RISK DETECTED")

            elif "HIGH" in risk_text:

                st.warning("🟠 HIGH RISK DETECTED")

            elif "MEDIUM" in risk_text:

                st.warning("🟡 MEDIUM RISK DETECTED")

            else:

                st.success("🟢 LOW RISK DETECTED")

        except Exception as e:

            st.error(f"Executive Summary Error: {e}")

# ---------------- USER INPUT ---------------- #

user_input = st.text_input(
    "Ask an intelligence question..."
)

# ---------------- AI ANALYSIS ---------------- #

if st.button("Analyze Intelligence"):

    if user_input.strip() == "":

        st.warning("Please enter a question.")

    else:

        if data_mode == "Incident Correlation":

            prompt = f"""
            You are an enterprise incident intelligence analyst.

            Correlate GitHub operational issues with Slack
            workspace intelligence and identify possible
            operational or security incidents.

            Correlated Data:
            {query_data}

            User Question:
            {user_input}

            Return response in this format:

            Incident Severity:
            (LOW / MEDIUM / HIGH / CRITICAL)

            Correlated Findings:
            - bullet points

            Possible Risks:
            - bullet points

            Recommended Actions:
            - bullet points

            Keep the response concise and enterprise-focused.
            """

        else:

            prompt = f"""
            You are an enterprise cybersecurity analyst.

            Analyze the following enterprise intelligence data.

            Intelligence Type:
            {data_mode}

            Retrieved Data:
            {query_data}

            User Question:
            {user_input}

            Return response in this format:

            Threat Level:
            (LOW / MEDIUM / HIGH / CRITICAL)

            Key Findings:
            - bullet points

            Risks Detected:
            - bullet points

            Recommended Actions:
            - bullet points

            Keep the response concise and professional.
            """

        # Send prompt to Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        response = chat_completion.choices[0].message.content

        st.write("## 🤖 AI Intelligence Analysis")

        if "CRITICAL" in response.upper():

            st.error(response)

        elif "HIGH" in response.upper():

            st.warning(response)

        else:

            st.success(response)