import re
import subprocess
import streamlit as st
from groq import Groq
import os
import streamlit.components.v1 as components
from dotenv import load_dotenv
from datetime import datetime

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RasmalAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:         #06080A;
    --surface:    #0D0F12;
    --surface2:   #131619;
    --border:     #1C2028;
    --border2:    #252B34;
    --gold:       #C8952E;
    --gold-dim:   #8B6420;
    --gold-bright:#E6B84A;
    --red:        #E05252;
    --orange:     #E07A40;
    --green:      #3DB87A;
    --blue:       #4A9EE0;
    --text:       #E8EAF0;
    --text-muted: #6B7280;
    --text-dim:   #9CA3AF;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

[data-testid="stAppViewContainer"] { background-color: var(--bg); }
[data-testid="stHeader"]           { background-color: var(--bg); height: 0px; }

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    background-color: var(--bg);
    max-width: 1400px;
}
.main { background-color: var(--bg) !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-dim) !important;
    font-size: 13px;
    font-family: 'IBM Plex Sans', sans-serif;
}
section[data-testid="stSidebar"] .stRadio label:hover { color: var(--gold-bright) !important; }
section[data-testid="stSidebar"] .stToggle label { font-size: 12px; color: var(--text-dim); }

/* ── CARDS ── */
.r-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.r-card-sm {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

/* ── SECTION LABELS ── */
.label {
    color: var(--gold);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── METRIC CARD ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; font-weight: 600;
    letter-spacing: 2px; color: var(--text-muted);
    text-transform: uppercase; margin-bottom: 8px;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px; font-weight: 700; line-height: 1;
}
.metric-sub { font-size: 11px; color: var(--text-muted); margin-top: 6px; }

/* ── SEVERITY BADGES ── */
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 600;
    letter-spacing: 1px; padding: 3px 8px;
    border-radius: 4px; text-transform: uppercase;
}
.badge-critical { background: rgba(224,82,82,0.15);   color: #E05252; border: 1px solid rgba(224,82,82,0.3);   }
.badge-high     { background: rgba(224,122,64,0.15);  color: #E07A40; border: 1px solid rgba(224,122,64,0.3);  }
.badge-medium   { background: rgba(200,149,46,0.15);  color: #C8952E; border: 1px solid rgba(200,149,46,0.3);  }
.badge-low      { background: rgba(61,184,122,0.15);  color: #3DB87A; border: 1px solid rgba(61,184,122,0.3);  }
.badge-open     { background: rgba(61,184,122,0.12);  color: #3DB87A; border: 1px solid rgba(61,184,122,0.25); }
.badge-closed   { background: rgba(107,114,128,0.15); color: #6B7280; border: 1px solid rgba(107,114,128,0.3); }

/* ── ADVISORY ROW ── */
.advisory-row {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px 16px; margin-bottom: 8px;
    display: flex; align-items: flex-start; gap: 14px;
}
.advisory-ghsa {
    font-family: 'IBM Plex Mono', monospace; font-size: 11px;
    color: var(--text-muted); margin-top: 4px; white-space: nowrap;
}
.advisory-summary { font-size: 14px; color: var(--text); line-height: 1.5; }

/* ── ISSUE ROW ── */
.issue-row {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
    display: flex; align-items: flex-start; gap: 12px;
}
.issue-title  { font-size: 14px; color: var(--text); font-weight: 500; }
.issue-meta   { font-size: 11px; color: var(--text-muted); margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }

/* ── SLACK BUBBLE ── */
.slack-msg {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;
}
.slack-msg-header {
    display: flex; align-items: center; gap: 10px; margin-bottom: 6px;
}
.slack-avatar {
    width: 28px; height: 28px; border-radius: 6px;
    background: var(--border2);
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace; font-size: 10px;
    font-weight: 700; color: var(--gold); flex-shrink: 0;
}
.slack-user  { font-size: 13px; font-weight: 600; color: var(--gold-bright); }
.slack-ts    { font-size: 11px; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; margin-left: auto; }
.slack-text  { font-size: 13px; color: var(--text-dim); line-height: 1.55; padding-left: 38px; word-break: break-word; }

/* ── CORRELATION CARD ── */
.corr-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 18px 20px; margin-bottom: 14px;
}
.corr-header {
    display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
    flex-wrap: wrap;
}
.corr-id {
    font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 700;
    color: var(--gold-bright); background: rgba(200,149,46,0.1);
    border: 1px solid rgba(200,149,46,0.2); border-radius: 5px; padding: 3px 10px;
}
.corr-field        { margin-bottom: 12px; }
.corr-field-label  {
    font-family: 'IBM Plex Mono', monospace; font-size: 9px; font-weight: 600;
    letter-spacing: 2px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;
}
.corr-field-value  { font-size: 13px; color: var(--text-dim); line-height: 1.5; }
.corr-action {
    background: var(--surface2); border: 1px solid var(--border2);
    border-radius: 8px; padding: 10px 14px; font-size: 13px;
    color: var(--text); font-weight: 500; margin-top: 10px;
    display: flex; align-items: flex-start; gap: 8px;
}

/* ── ANALYSIS RESPONSE ── */
.analysis-response {
    background: var(--surface2); border: 1px solid var(--border2);
    border-radius: 10px; padding: 18px 20px; font-size: 14px;
    color: var(--text-dim); line-height: 1.7; margin-top: 14px; white-space: pre-wrap;
}

/* ── SUMMARY CARD ── */
.summary-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 22px 24px; margin-bottom: 14px;
}
.summary-card.critical { border-left: 3px solid var(--red); }
.summary-card.high     { border-left: 3px solid var(--orange); }
.summary-card.elevated { border-left: 3px solid var(--gold); }
.summary-card.nominal  { border-left: 3px solid var(--green); }
.summary-field-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 9px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;
}
.summary-threat {
    font-family: 'IBM Plex Mono', monospace; font-size: 32px;
    font-weight: 700; margin-bottom: 18px;
}
.summary-text { font-size: 14px; color: var(--text-dim); line-height: 1.65; }

/* ── ACTION ITEM ── */
.action-item {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
    display: flex; gap: 12px; align-items: flex-start;
}
.action-num {
    font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 700;
    color: var(--gold); background: rgba(200,149,46,0.1);
    border: 1px solid rgba(200,149,46,0.2); border-radius: 4px;
    padding: 2px 7px; flex-shrink: 0; margin-top: 1px;
}
.action-text { font-size: 13px; color: var(--text-dim); line-height: 1.55; }

/* ── DIVIDER ── */
.divider { border: none; border-top: 1px solid var(--border); margin: 20px 0; }

/* ── BUTTONS ── */
div.stButton > button {
    background: var(--gold); color: #06080A; border: none;
    border-radius: 8px; font-weight: 700; font-size: 13px;
    font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.5px;
    padding: 0.6rem 1rem; width: 100%; transition: background 0.15s;
}
div.stButton > button:hover { background: var(--gold-bright); }

/* ── INPUT ── */
.stTextInput input {
    background: var(--surface2) !important; color: var(--text) !important;
    border: 1px solid var(--border2) !important; border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important; font-size: 14px !important;
}
.stTextInput input::placeholder { color: var(--text-muted) !important; }
.stTextInput input:focus { border-color: var(--gold-dim) !important; }

/* ── EXPANDER ── */
.stExpander { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
.stExpander summary { color: var(--text-muted) !important; font-size: 12px; }
pre, code {
    background: var(--surface2) !important; color: var(--text-dim) !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important;
}

/* ── PULSE ── */
@keyframes pulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }
.pulse { animation: pulse 2s infinite; }

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def run_coral_query(query):
    result = subprocess.run(["coral", "sql", query], capture_output=True, text=True)
    if result.returncode != 0:
        error_detail = result.stderr.strip() or "No error details returned."
        return f"ERROR (exit code {result.returncode}):\n{error_detail}"
    return result.stdout


def clean_llm_output(text):
    return (
        text
        .replace("**", "").replace("*", "")
        .replace("##", "").replace("#", "")
        .replace("__", "").replace("`", "")
    )


def extract_field(text, *keys):
    for key in keys:
        escaped = re.escape(key)
        pattern = r"(?i)" + escaped + r"\s*[:\-]?\s*([^\n]+)"
        match = re.search(pattern, text)
        if match:
            val = match.group(1).strip().strip(":- ")
            if val:
                return val
    return ""


def severity_badge(sev):
    sev = (sev or "").strip().lower()
    if "critical" in sev:
        return '<span class="badge badge-critical">CRITICAL</span>'
    elif "high" in sev:
        return '<span class="badge badge-high">HIGH</span>'
    elif "medium" in sev or "moderate" in sev:
        return '<span class="badge badge-medium">MEDIUM</span>'
    elif "low" in sev:
        return '<span class="badge badge-low">LOW</span>'
    return '<span class="badge badge-low">UNKNOWN</span>'


def state_badge(state):
    state = (state or "").strip().lower()
    if "open" in state:
        return '<span class="badge badge-open">OPEN</span>'
    return '<span class="badge badge-closed">CLOSED</span>'


def parse_coral_rows(raw):
    """
    Parse coral SQL tabular output into (headers, rows).
    Supports pipe-delimited format:  | col1 | col2 | col3 |
    Also supports plain separator lines like +------+------+
    Returns (list_of_header_strings, list_of_dicts).
    """
    if not raw or raw.startswith("ERROR"):
        return [], []

    lines = raw.strip().splitlines()
    headers = []
    rows = []
    header_found = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Separator line — skip
        if re.match(r'^[+\-|=\s]+$', stripped):
            continue

        # Pipe-delimited content line
        if '|' in stripped:
            # Split on | and strip each cell
            cells = [c.strip() for c in stripped.split('|')]
            # Remove leading/trailing empty strings from outer pipes
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]

            if not cells:
                continue

            if not header_found:
                headers = cells
                header_found = True
            else:
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells)))
                elif cells:
                    # Pad or truncate to match headers
                    padded = (cells + [''] * len(headers))[:len(headers)]
                    rows.append(dict(zip(headers, padded)))

    return headers, rows


def format_slack_ts(ts_str):
    """Convert Slack unix timestamp string to readable time."""
    try:
        # Slack timestamps look like "1716544253.587139"
        ts = float(ts_str)
        return datetime.fromtimestamp(ts).strftime("%b %d, %H:%M")
    except Exception:
        # Not a number — return as-is, trimmed
        return (ts_str or "")[:16]


def resolve_slack_users(user_ids):
    """
    Try to resolve a list of Slack user IDs to real display names via Coral.
    Falls back to numbered aliases (User-1, User-2, ...) if the query fails
    or returns no useful data.
    Returns a dict: {uid: display_name}
    """
    mapping = {}
    if not user_ids:
        return mapping

    # Attempt Coral lookup for real names
    try:
        ids_csv = ", ".join(f"'{u}'" for u in user_ids if u)
        raw = run_coral_query(f"""
            SELECT id, display_name, real_name, name
            FROM slack.users
            WHERE id IN ({ids_csv})
        """)
        if not raw.startswith("ERROR"):
            _, rows = parse_coral_rows(raw)
            for row in rows:
                uid  = row.get("id", "").strip()
                name = (
                    row.get("display_name", "").strip()
                    or row.get("real_name", "").strip()
                    or row.get("name", "").strip()
                )
                if uid and name:
                    mapping[uid] = name
    except Exception:
        pass

    # Fallback: assign sequential friendly aliases for any uid not resolved
    counter = 1
    for uid in user_ids:
        if uid and uid not in mapping:
            mapping[uid] = f"User-{counter}"
            counter += 1

    return mapping


def slack_display_name(uid, user_map=None):
    """Return a readable display name for a Slack user ID."""
    if not uid:
        return "Unknown"
    uid = uid.strip()
    if user_map and uid in user_map:
        return user_map[uid]
    return uid  # last-resort fallback


def user_initials(display_name):
    """
    Derive 2-char initials from a resolved display name.
    'Alice Smith' -> 'AS', 'User-3' -> 'U3', single word -> first 2 chars.
    """
    if not display_name:
        return "??"
    name = display_name.strip()

    # Numbered alias like User-3 -> U3
    m = re.match(r'^User-(\d+)$', name)
    if m:
        return f"U{m.group(1)}"

    # Real name with space: first letters of first two words
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    if len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()
    return name[:2].upper()


# =========================================================
# RISK SCORING HELPER
# =========================================================

def calculate_risk(raw_text):
    """
    Compute risk score from structured data rather than raw string counting.
    Counts distinct advisory severities and incident-related keywords carefully
    to avoid inflating the score just because the word 'critical' appears in data.
    """
    text_lower = raw_text.lower()

    # Count unique advisories at each severity (not raw occurrences)
    critical_advisories = len(re.findall(r'\bcritical\b', text_lower))
    high_advisories     = len(re.findall(r'\bhigh\b', text_lower))

    # Count incident signal keywords — but cap contribution so one verbose
    # advisory doesn't push score to CRITICAL on its own
    signal_keywords = [
        "outage", "incident", "rollback", "breach", "exploit",
        "unauthorized", "attack", "failure"
    ]
    signal_hits = sum(1 for kw in signal_keywords if kw in text_lower)

    # Score: advisories contribute proportionally, signals add urgency
    score = (critical_advisories * 15) + (high_advisories * 6) + (signal_hits * 10)
    score = min(score, 100)

    active_signals = critical_advisories + high_advisories + signal_hits
    correlation_conf = min(50 + signal_hits * 5 + critical_advisories * 3, 97)

    if score >= 75:
        level, color = "CRITICAL", "#E05252"
    elif score >= 45:
        level, color = "HIGH",     "#E07A40"
    elif score >= 20:
        level, color = "ELEVATED", "#C8952E"
    else:
        level, color = "NOMINAL",  "#3DB87A"

    return level, color, score, active_signals, correlation_conf


# =========================================================
# SIDEBAR
# =========================================================

slack_channels = {
    "prod-incidents":  "C0B5LPBQSDR",
    "security-alerts": "C0B5WNUL6A0",
    "backend-team":    "C0B5V016BT3",
}

# Initialise variables that are only set inside sidebar branches
# so the rest of the page never hits a NameError
github_mode      = "Security Advisories"
show_all_severity = True
selected_channel  = list(slack_channels.keys())[0]

with st.sidebar:
    st.markdown("""
    <div style="padding:14px 0 6px 0;">
        <div style="color:#E6B84A;font-size:17px;font-weight:800;letter-spacing:0.5px;
                    font-family:'IBM Plex Mono',monospace;">⚡ RasmalAI</div>
        <div style="color:#4B5563;font-size:9px;letter-spacing:2px;margin-top:3px;
                    font-family:'IBM Plex Mono',monospace;text-transform:uppercase;">
            Intelligence Command
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #1C2028;margin:10px 0 16px 0;">
    """, unsafe_allow_html=True)

    st.markdown('<div class="label" style="margin-bottom:8px;">Mode</div>', unsafe_allow_html=True)

    main_mode = st.radio(
        label="mode",
        options=["GitHub Intelligence", "Slack Intelligence", "Incident Correlation"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border:none;border-top:1px solid #1C2028;margin:14px 0;'>", unsafe_allow_html=True)

    if main_mode == "GitHub Intelligence":
        st.markdown('<div class="label" style="margin-bottom:8px;">Subsystem</div>', unsafe_allow_html=True)
        github_mode = st.radio(
            label="github_subsystem",
            options=["Security Advisories", "Repository Issues"],
            label_visibility="collapsed"
        )
        if github_mode == "Security Advisories":
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            show_all_severity = st.toggle("Show all severities", value=True)

    elif main_mode == "Slack Intelligence":
        st.markdown('<div class="label" style="margin-bottom:8px;">Channel</div>', unsafe_allow_html=True)
        selected_channel = st.radio(
            label="slack_channel",
            options=list(slack_channels.keys()),
            label_visibility="collapsed"
        )

# =========================================================
# COMPACT HEADER
# =========================================================

hcol1, hcol2 = st.columns([5, 2])

with hcol1:
    logo_col, text_col = st.columns([1, 8])
    with logo_col:
        st.image(logo_path, width=5000)
    with text_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:14px;padding-top:2px;">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:22px;
                         font-weight:800;color:#E6B84A;letter-spacing:1px;">RasmalAI</span>
            <span style="color:#1C2028;font-size:18px;">|</span>
            <span style="font-size:13px;color:#6B7280;font-weight:400;">
                AI-Powered Security Intelligence
            </span>
        </div>
        """, unsafe_allow_html=True)

with hcol2:
    components.html("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: transparent; }
    .clock-wrap {
        display: flex; align-items: center; gap: 10px;
        background: #0D0F12; border: 1px solid #1C2028;
        border-radius: 8px; padding: 8px 14px; margin-top: 2px;
    }
    .dot { width:7px; height:7px; border-radius:50%; background:#3DB87A; animation:pulse 2s infinite; flex-shrink:0; }
    @keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:1} }
    #clock { font-family:'IBM Plex Mono',monospace; font-size:16px; font-weight:700; color:#E6B84A; letter-spacing:1px; }
    .node  { font-family:'IBM Plex Mono',monospace; font-size:9px; color:#4B5563; letter-spacing:1.5px; text-transform:uppercase; margin-left:auto; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@700&display=swap" rel="stylesheet">
    <div class="clock-wrap">
        <div class="dot"></div>
        <span id="clock">--:--:--</span>
        <span class="node">NODE_ACTIVE</span>
    </div>
    <script>
    function tick() {
        const now = new Date();
        document.getElementById('clock').textContent =
            String(now.getHours()).padStart(2,'0') + ':' +
            String(now.getMinutes()).padStart(2,'0') + ':' +
            String(now.getSeconds()).padStart(2,'0');
    }
    tick(); setInterval(tick, 1000);
    </script>
    """, height=46)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# =========================================================
# DATA FETCHING + RENDERED UI — per mode
# =========================================================

query_data = ""

# ----------------------------------------------------------
# GITHUB — SECURITY ADVISORIES
# ----------------------------------------------------------

if main_mode == "GitHub Intelligence" and github_mode == "Security Advisories":

    raw = run_coral_query("""
        SELECT ghsa_id, summary, severity
        FROM github.advisories
        LIMIT 20
    """)

    if not show_all_severity:
        filtered = [
            line for line in raw.splitlines()
            if "critical" in line.lower() or "high" in line.lower()
        ]
        query_data = "\n".join(filtered) if filtered else raw
    else:
        query_data = raw

    headers, rows = parse_coral_rows(query_data)

    st.markdown('<div class="label">Security Advisories</div>', unsafe_allow_html=True)

    if raw.startswith("ERROR"):
        st.markdown(f"""
        <div class="r-card" style="border-left:3px solid #E05252;">
            <div style="color:#E05252;font-size:13px;font-weight:600;">Query Error</div>
            <div style="color:#6B7280;font-size:12px;margin-top:6px;">{raw}</div>
        </div>
        """, unsafe_allow_html=True)
    elif not rows:
        st.markdown("""
        <div class="r-card">
            <div style="color:#6B7280;font-size:13px;">No advisories returned.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Identify columns by matching header names
        ghsa_col = next((h for h in headers if "ghsa" in h.lower()), None) or headers[0]
        sev_col  = next((h for h in headers if "sev" in h.lower()), None)
        sum_col  = next((h for h in headers if "sum" in h.lower() or "desc" in h.lower()), None)
        # Fallback: use whichever columns exist
        if not sev_col and len(headers) >= 3:
            sev_col = headers[2]
        if not sum_col and len(headers) >= 2:
            sum_col = headers[1]

        for row in rows:
            ghsa    = row.get(ghsa_col, "")
            sev     = row.get(sev_col, "") if sev_col else ""
            summary = row.get(sum_col, "") if sum_col else ""
            if not summary:
                summary = " | ".join(v for v in row.values() if v != ghsa and v != sev)
            st.markdown(
                f'<div class="advisory-row">'
                f'  <div style="padding-top:2px;">{severity_badge(sev)}</div>'
                f'  <div style="flex:1;">'
                f'    <div class="advisory-summary">{summary}</div>'
                f'    <div class="advisory-ghsa">{ghsa}</div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ----------------------------------------------------------
# GITHUB — REPOSITORY ISSUES
# ----------------------------------------------------------

elif main_mode == "GitHub Intelligence" and github_mode == "Repository Issues":

    raw = run_coral_query("""
        SELECT id, title, state, user__login, created_at
        FROM github.issues
        WHERE owner = 'uk-repack'
        AND repo = 'RasmalAI'
        LIMIT 10
    """)
    query_data = raw

    alert_kw = ["critical", "outage", "authentication", "failure", "exploit", "breach", "unauthorized"]
    headers, rows = parse_coral_rows(raw)

    st.markdown('<div class="label">Repository Issues</div>', unsafe_allow_html=True)

    if raw.startswith("ERROR"):
        st.markdown(f"""
        <div class="r-card" style="border-left:3px solid #E05252;">
            <div style="color:#E05252;font-size:13px;font-weight:600;">Query Error</div>
            <div style="color:#6B7280;font-size:12px;margin-top:6px;">{raw}</div>
        </div>
        """, unsafe_allow_html=True)
    elif not rows:
        st.markdown("""
        <div class="r-card">
            <div style="color:#6B7280;font-size:13px;">No issues found.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        id_col    = next((h for h in headers if h.lower() in ("id", "#", "number")), headers[0])
        title_col = next((h for h in headers if "title" in h.lower()), headers[1] if len(headers) > 1 else headers[0])
        state_col = next((h for h in headers if "state" in h.lower()), None)
        user_col  = next((h for h in headers if "login" in h.lower() or "user" in h.lower()), None)
        date_col  = next((h for h in headers if "created" in h.lower() or "date" in h.lower()), None)

        for row in rows:
            iid     = row.get(id_col, "")
            title   = row.get(title_col, "") or next(iter(row.values()), "")
            state   = row.get(state_col, "open") if state_col else "open"
            user    = row.get(user_col, "") if user_col else ""
            date    = row.get(date_col, "") if date_col else ""
            flagged = any(kw in title.lower() for kw in alert_kw)
            date_short = date[:10] if date else ""

            flag_span = '<span style="color:#E05252;font-size:11px;margin-left:auto;font-family:\'IBM Plex Mono\',monospace;font-weight:700;">⚠ FLAGGED</span>' if flagged else ''
            border    = "border-left:3px solid #E05252;" if flagged else ""
            meta_parts = [p for p in [("#" + iid if iid else ""), user, date_short] if p]
            meta_str   = " · ".join(meta_parts)

            st.markdown(
                f'<div class="issue-row" style="{border}">'
                f'  <div style="flex:1;">'
                f'    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
                f'      {state_badge(state)}'
                f'      <span class="issue-title">{title}</span>'
                f'      {flag_span}'
                f'    </div>'
                f'    <div class="issue-meta">{meta_str}</div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ----------------------------------------------------------
# SLACK INTELLIGENCE
# ----------------------------------------------------------

elif main_mode == "Slack Intelligence":

    channel_id = slack_channels[selected_channel]

    raw = run_coral_query(f"""
        SELECT ts, user_id, text
        FROM slack.messages(channel => '{channel_id}')
        ORDER BY ts DESC
        LIMIT 12
    """)
    query_data = raw

    st.markdown(f'<div class="label">#{selected_channel}</div>', unsafe_allow_html=True)

    if raw.startswith("ERROR"):
        st.markdown(
            f'<div class="r-card" style="border-left:3px solid #C8952E;">'
            f'  <div style="color:#C8952E;font-size:13px;font-weight:600;margin-bottom:6px;">⚠ Channel Unavailable</div>'
            f'  <div style="color:#6B7280;font-size:12px;">Channel <code>#{selected_channel}</code> (ID: {channel_id}) '
            f'  could not be queried. It may be archived or the ID may have changed.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        headers, rows = parse_coral_rows(raw)

        if not rows:
            st.markdown("""
            <div class="r-card">
                <div style="color:#6B7280;font-size:13px;">No messages returned.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # BUG FIX: detect columns by checking for 'user_id' specifically, not just 'user'
            ts_col   = next((h for h in headers if h.lower() in ("ts", "timestamp", "time")), None)
            user_col = next((h for h in headers if h.lower() in ("user_id", "user", "userid", "from")), None)
            text_col = next((h for h in headers if h.lower() in ("text", "message", "msg", "body")), None)
            # Final fallbacks by position
            if ts_col   is None and len(headers) >= 1: ts_col   = headers[0]
            if user_col is None and len(headers) >= 2: user_col = headers[1]
            if text_col is None and len(headers) >= 3: text_col = headers[2]

            # Resolve all user IDs to real names (or friendly aliases) in one shot
            all_uids = list(dict.fromkeys(
                row.get(user_col, "") for row in rows if user_col
            ))
            user_map = resolve_slack_users([u for u in all_uids if u])

            for row in rows:
                ts_raw  = row.get(ts_col, "")   if ts_col   else ""
                uid     = row.get(user_col, "")  if user_col else ""
                text    = row.get(text_col, "")  if text_col else " ".join(row.values())

                ts_fmt       = format_slack_ts(ts_raw)
                display_name = slack_display_name(uid, user_map)
                initials     = user_initials(display_name)

                # Escape any HTML in the message text to prevent injection
                safe_text = (text
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))

                st.markdown(
                    f'<div class="slack-msg">'
                    f'  <div class="slack-msg-header">'
                    f'    <div class="slack-avatar">{initials}</div>'
                    f'    <span class="slack-user">{display_name}</span>'
                    f'    <span class="slack-ts">{ts_fmt}</span>'
                    f'  </div>'
                    f'  <div class="slack-text">{safe_text}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# ----------------------------------------------------------
# INCIDENT CORRELATION
# ----------------------------------------------------------

else:

    pr_query = """
        SELECT id, title, state, user__login, created_at
        FROM github.issues
        WHERE owner = 'uk-repack' AND repo = 'RasmalAI'
        LIMIT 5
    """
    issues_query = """
        SELECT id, title, state, user__login, created_at
        FROM github.issues
        WHERE owner = 'uk-repack' AND repo = 'RasmalAI' AND state = 'open'
        LIMIT 8
    """
    advisory_query = """
        SELECT ghsa_id, summary, severity
        FROM github.advisories LIMIT 6
    """
    incidents_query = """
        SELECT ts, user_id, text
        FROM slack.messages(channel => 'C0B5LPBQSDR')
        ORDER BY ts DESC LIMIT 10
    """
    security_query = """
        SELECT ts, user_id, text
        FROM slack.messages(channel => 'C0B5WNUL6A0')
        ORDER BY ts DESC LIMIT 8
    """

    with st.spinner("Pulling intelligence feeds..."):
        pr_results        = run_coral_query(pr_query)
        issues_results    = run_coral_query(issues_query)
        advisory_results  = run_coral_query(advisory_query)
        incidents_results = run_coral_query(incidents_query)
        security_results  = run_coral_query(security_query)

    query_data = "\n".join([
        "RECENT PULL REQUESTS / DEPLOYS", pr_results,
        "OPEN REPOSITORY ISSUES",         issues_results,
        "GITHUB SECURITY ADVISORIES",     advisory_results,
        "SLACK #prod-incidents",          incidents_results,
        "SLACK #security-alerts",         security_results,
    ])

    correlation_prompt = f"""You are a senior on-call engineer doing incident triage.
You have live data from three sources from the last 24 hours.

--- RECENT PULL REQUESTS / DEPLOYS ---
{pr_results}

--- OPEN REPOSITORY ISSUES ---
{issues_results}

--- GITHUB SECURITY ADVISORIES ---
{advisory_results}

--- SLACK #prod-incidents ---
{incidents_results}

--- SLACK #security-alerts ---
{security_results}

Find real causal or temporal links that NO single source reveals alone.

For each correlation output EXACTLY this block (repeat per match, no extra text between blocks):

CORRELATION_ID: C01
TYPE: advisory-match
CONFIDENCE: high
CONFIDENCE_REASON: one sentence only
TIMELINE: what happened first, then second, then third
BLAST_RADIUS: affected services or systems
RECOMMENDED_ACTION: one concrete immediate step

Rules:
- Only output correlations with specific evidence from the data above.
- If no genuine correlations exist output exactly: NO_CORRELATIONS_FOUND
- Do not invent data. Do not hallucinate timestamps. Be falsifiable.
- Plain text only. No markdown. No bullet points. No HTML.
"""

    st.markdown('<div class="label">Deploy Regression Detector</div>', unsafe_allow_html=True)

    try:
        with st.spinner("Running correlation engine..."):
            corr_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": correlation_prompt}],
                model="llama-3.3-70b-versatile"
            )

        # BUG FIX: clean the output BEFORE we try to render it — the LLM sometimes
        # returns HTML tags or markdown that then gets injected into our own HTML
        raw_corr = corr_completion.choices[0].message.content or ""
        # Strip any HTML tags the LLM might have hallucinated
        raw_corr = re.sub(r'<[^>]+>', '', raw_corr)
        correlation_output = clean_llm_output(raw_corr)

        no_corr = "NO_CORRELATIONS_FOUND" in correlation_output.upper()

        if no_corr:
            st.markdown(
                '<div class="r-card" style="border-left:3px solid #3DB87A;">'
                '  <div style="display:flex;align-items:center;gap:10px;">'
                '    <span style="color:#3DB87A;font-size:18px;">✓</span>'
                '    <span style="color:#3DB87A;font-size:14px;font-weight:600;">'
                '      No cross-source correlations detected'
                '    </span>'
                '  </div>'
                '  <div style="color:#6B7280;font-size:12px;margin-top:8px;">'
                '    All feeds are clean — no matching signals in this time window.'
                '  </div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            blocks = re.split(r"(?=CORRELATION_ID\s*:)", correlation_output.strip())
            blocks = [b.strip() for b in blocks if b.strip() and "CORRELATION_ID" in b]

            if not blocks:
                # No parseable blocks — show raw text in a safe container
                safe_output = (correlation_output
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))
                st.markdown(
                    f'<div class="r-card">'
                    f'  <div style="color:#9CA3AF;font-size:13px;line-height:1.8;white-space:pre-wrap;">{safe_output}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            def _ext(text, field):
                m = re.search(r"(?i)" + re.escape(field) + r"\s*:\s*([^\n]+)", text)
                return (m.group(1).strip() if m else "—")

            for block in blocks:
                cid         = _ext(block, "CORRELATION_ID")
                ctype       = _ext(block, "TYPE")
                confidence  = _ext(block, "CONFIDENCE").upper()
                conf_reason = _ext(block, "CONFIDENCE_REASON")
                timeline    = _ext(block, "TIMELINE")
                blast       = _ext(block, "BLAST_RADIUS")
                action      = _ext(block, "RECOMMENDED_ACTION")

                conf_color = (
                    "#E05252" if confidence == "HIGH"
                    else "#E07A40" if confidence == "MEDIUM"
                    else "#C8952E"
                )
                type_colors = {
                    "deploy-regression":     ("#E05252", "rgba(224,82,82,0.12)"),
                    "advisory-match":        ("#E07A40", "rgba(224,122,64,0.12)"),
                    "slack-advisory-overlap":("#C8952E", "rgba(200,149,46,0.12)"),
                }
                tc, tbg = type_colors.get(ctype.lower(), ("#9CA3AF", "rgba(107,114,128,0.1)"))

                # BUG FIX: build the HTML via a list of safe strings,
                # never inserting un-escaped LLM output into attribute positions
                def safe(s):
                    return (s or "—").replace("<","&lt;").replace(">","&gt;").replace("&","&amp;")

                st.markdown(
                    f'<div class="corr-card" style="border-left:3px solid {conf_color};">'
                    f'  <div class="corr-header">'
                    f'    <span class="corr-id">{safe(cid)}</span>'
                    f'    <span style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;font-weight:600;'
                    f'           letter-spacing:1px;padding:3px 9px;border-radius:4px;'
                    f'           background:{tbg};color:{tc};border:1px solid {tc}33;">'
                    f'      {safe(ctype).upper()}'
                    f'    </span>'
                    f'    <span style="margin-left:auto;font-family:\'IBM Plex Mono\',monospace;'
                    f'           font-size:10px;font-weight:700;color:{conf_color};letter-spacing:1px;">'
                    f'      {safe(confidence)} CONFIDENCE'
                    f'    </span>'
                    f'  </div>'
                    f'  <div class="corr-field">'
                    f'    <div class="corr-field-label">Why this confidence</div>'
                    f'    <div class="corr-field-value">{safe(conf_reason)}</div>'
                    f'  </div>'
                    f'  <div class="corr-field">'
                    f'    <div class="corr-field-label">Timeline</div>'
                    f'    <div class="corr-field-value">{safe(timeline)}</div>'
                    f'  </div>'
                    f'  <div class="corr-field">'
                    f'    <div class="corr-field-label">Blast Radius</div>'
                    f'    <div class="corr-field-value">{safe(blast)}</div>'
                    f'  </div>'
                    f'  <div class="corr-action">'
                    f'    <span style="color:#C8952E;font-size:14px;flex-shrink:0;">&#8594;</span>'
                    f'    <span>{safe(action)}</span>'
                    f'  </div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.markdown(
            f'<div class="r-card" style="border-left:3px solid #E05252;">'
            f'  <div style="color:#E05252;font-size:13px;">Correlation Engine Error: {e}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

# Fallback
if not query_data or not query_data.strip():
    query_data = "NO_DATA: No intelligence data returned for the selected mode."

# =========================================================
# RISK SCORING (runs after data is fetched)
# =========================================================

risk_level, risk_color, risk_score, active_signals, correlation_confidence = calculate_risk(query_data)
system_status = "OBSERVING" if risk_level in ("CRITICAL", "HIGH") else "STABLE"
status_color  = "#E07A40" if system_status == "OBSERVING" else "#3DB87A"

# =========================================================
# METRICS BAR — context-sensitive (no Correlation Confidence on single-source views)
# =========================================================

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

if main_mode == "Incident Correlation":
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Risk Index</div>'
            f'<div class="metric-value" style="color:{risk_color};">{risk_level}</div></div>',
            unsafe_allow_html=True)
    with m2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Correlation Confidence</div>'
            f'<div class="metric-value" style="color:#C8952E;">{correlation_confidence}%</div></div>',
            unsafe_allow_html=True)
    with m3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Active Signals</div>'
            f'<div class="metric-value" style="color:#C8952E;">{active_signals}</div></div>',
            unsafe_allow_html=True)
    with m4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">System Status</div>'
            f'<div class="metric-value" style="font-size:22px;color:{status_color};">{system_status}</div></div>',
            unsafe_allow_html=True)

elif main_mode == "GitHub Intelligence":
    m1, m2, m3 = st.columns(3)
    _, adv_rows = parse_coral_rows(query_data)
    if github_mode == "Security Advisories":
        adv_count  = len(adv_rows) if adv_rows else query_data.count("GHSA-")
        sev_h      = next((h for h in (adv_rows[0].keys() if adv_rows else []) if "sev" in h.lower()), "")
        crit_adv   = sum(1 for r in adv_rows if "critical" in r.get(sev_h,"").lower()) if sev_h else 0
        high_adv   = sum(1 for r in adv_rows if "high"     in r.get(sev_h,"").lower()) if sev_h else 0
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Index</div><div class="metric-value" style="color:{risk_color};">{risk_level}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Advisories Loaded</div><div class="metric-value" style="color:#C8952E;">{adv_count}</div><div class="metric-sub">{crit_adv} critical · {high_adv} high</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">System Status</div><div class="metric-value" style="font-size:22px;color:{status_color};">{system_status}</div></div>', unsafe_allow_html=True)
    else:
        issue_count = len(adv_rows)
        st_h = next((h for h in (adv_rows[0].keys() if adv_rows else []) if "state" in h.lower()), "")
        open_count  = sum(1 for r in adv_rows if "open" in r.get(st_h,"").lower()) if st_h else 0
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Index</div><div class="metric-value" style="color:{risk_color};">{risk_level}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Issues Found</div><div class="metric-value" style="color:#C8952E;">{issue_count}</div><div class="metric-sub">{open_count} open</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">System Status</div><div class="metric-value" style="font-size:22px;color:{status_color};">{system_status}</div></div>', unsafe_allow_html=True)

else:  # Slack Intelligence — selected_channel is always defined here
    _, s_rows = parse_coral_rows(query_data)
    msg_count = len(s_rows) if s_rows else max(0, query_data.count("\n") - 4)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Index</div><div class="metric-value" style="color:{risk_color};">{risk_level}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Messages Loaded</div><div class="metric-value" style="color:#C8952E;">{msg_count}</div><div class="metric-sub">#{selected_channel}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Active Signals</div><div class="metric-value" style="color:#C8952E;">{active_signals}</div></div>', unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# =========================================================
# EXECUTIVE INTELLIGENCE SUMMARY
# =========================================================

st.markdown('<div class="label">Executive Intelligence Summary</div>', unsafe_allow_html=True)

if st.button("Generate Executive Summary"):
    prompt = f"""You are RasmalAI, an elite cyber intelligence platform.

Operational Intelligence:
{query_data}

Risk Level: {risk_level}

Return ONLY in this exact structure — no extra text, no markdown:

THREAT_LEVEL:
(one word: CRITICAL, HIGH, ELEVATED, or NOMINAL)

PRIMARY_CONCERN:
(1 concise sentence)

IMPACT:
(1 concise operational impact sentence)

IMMEDIATE_ACTIONS:
- short bullet
- short bullet
- short bullet
"""
    try:
        with st.spinner("Generating executive summary..."):
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )

        summary = clean_llm_output(completion.choices[0].message.content)

        threat_level    = extract_field(summary, "THREAT_LEVEL", "THREAT LEVEL", "Threat Level")
        primary_concern = extract_field(summary, "PRIMARY_CONCERN", "PRIMARY CONCERN", "Primary Concern")
        impact          = extract_field(summary, "IMPACT", "OPERATIONAL IMPACT", "Operational Impact")
        action_pattern  = re.compile(r"^\s*[-*•]\s*(.+)", re.MULTILINE)
        actions = [m.group(1).strip() for m in action_pattern.finditer(summary)]

        threat_level    = threat_level    or "UNKNOWN"
        primary_concern = primary_concern or "No intelligence available"
        impact          = impact          or "No intelligence available"

        tl_up = threat_level.upper()
        if "CRITICAL" in tl_up:
            sev_class, sev_color = "critical", "#E05252"
        elif "HIGH" in tl_up:
            sev_class, sev_color = "high",     "#E07A40"
        elif "ELEVATED" in tl_up:
            sev_class, sev_color = "elevated", "#C8952E"
        else:
            sev_class, sev_color = "nominal",  "#3DB87A"

        st.markdown(
            f'<div class="summary-card {sev_class}">'
            f'  <div class="summary-field-label">Threat Severity</div>'
            f'  <div class="summary-threat" style="color:{sev_color};">{threat_level}</div>'
            f'  <div class="summary-field-label">Primary Concern</div>'
            f'  <div class="summary-text" style="margin-bottom:14px;">{primary_concern}</div>'
            f'  <div class="summary-field-label">Operational Impact</div>'
            f'  <div class="summary-text">{impact}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if actions:
            st.markdown('<div class="label" style="margin-top:16px;">Immediate Response Actions</div>', unsafe_allow_html=True)
            for idx, action in enumerate(actions):
                st.markdown(
                    f'<div class="action-item">'
                    f'  <div class="action-num">P{idx+1}</div>'
                    f'  <div class="action-text">{action}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.markdown(f'<div class="r-card" style="border-left:3px solid #E05252;"><div style="color:#E05252;font-size:13px;">Summary Error: {e}</div></div>', unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# =========================================================
# ANALYSIS ENGINE
# =========================================================

st.markdown('<div class="label">Analysis Engine</div>', unsafe_allow_html=True)

user_input = st.text_input(
    "Ask RasmalAI about the current intelligence...",
    placeholder="e.g. Which advisory is most likely to affect our auth service?"
)

if st.button("Run Analysis"):
    if not user_input.strip():
        st.markdown('<div class="r-card" style="border-left:3px solid #C8952E;"><div style="color:#C8952E;font-size:13px;">Please enter a question.</div></div>', unsafe_allow_html=True)
    else:
        prompt = f"""You are RasmalAI, an elite AI security intelligence platform.

Operational context (current risk level: {risk_level}):
{query_data}

Answer this question directly and concisely:
{user_input}

Be specific to the data provided. If the data is insufficient, say so briefly.
No section headers. No forced structure. Just answer the question."""

        with st.spinner("Running analysis..."):
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                response = clean_llm_output(completion.choices[0].message.content)
            except Exception as e:
                st.markdown(f'<div class="r-card" style="border-left:3px solid #E05252;"><div style="color:#E05252;font-size:13px;">Analysis Engine Error: {e}</div></div>', unsafe_allow_html=True)
                st.stop()

        # Neutral styled box — color NOT based on risk level
        safe_resp = response.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        st.markdown(f'<div class="analysis-response">{safe_resp}</div>', unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# =========================================================
# RAW DATA EXPANDER — always at bottom
# =========================================================

with st.expander("View Raw Intelligence Data"):
    st.code(query_data, language="text")
