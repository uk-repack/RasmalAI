# RasmalAI

Real-time incident correlation engine. Pulls live data from GitHub and Slack, finds causal links across deploys, incidents, and security advisories using AI.

**[Live Demo](https://rasmalai-production.up.railway.app/) · [Coral Atlas](https://coral-atlas-query-ex-26t5.bolt.host/) · [Discord](https://discord.gg/XvpGtxQxX)**

---

## What it does

When a deploy merges, an incident fires in Slack, and a CVE drops in the advisory feed — RasmalAI tells you if they're connected and why, before you've opened your third browser tab.

Three intelligence modes:

- **Deploy Regression Detector** — correlates merged PRs against Slack incident messages by timing proximity, service name overlap, and error keywords. Outputs structured findings with confidence level, affected system, blast radius, and a single recommended action.
- **Threat Intelligence Feed** — queries the GitHub Advisory Database live. Filters to CRITICAL and HIGH severity by default.
- **Slack Channel Monitor** — pulls recent messages from `prod-incidents` and `security-alerts`, surfaces repeated failure patterns.

---

## Architecture

| Layer | Technology |
|-------|-----------|
| Data | [Coral](https://withcoral.com) — SQL interface over live SaaS APIs |
| Inference | Groq · LLaMA 3.3 70B |
| UI | Streamlit |

### Data layer

All data fetching goes through one function:

```python
def run_coral_query(query):
    result = subprocess.run(
        ["coral", "sql", query],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_detail = result.stderr.strip() or "No error details returned."
        return f"ERROR (exit code {result.returncode}):\n{error_detail}"
    return result.stdout
```

**GitHub advisories:**
```sql
SELECT ghsa_id, summary, severity
FROM github.advisories
LIMIT 8
```

**GitHub repo activity:**
```sql
SELECT id, title, state, user__login, created_at
FROM github.issues
WHERE owner = 'uk-repack'
AND repo = 'RasmalAI'
LIMIT 10
```

> `WHERE owner` and `WHERE repo` are mandatory. Omitting them returns zero rows silently.  
> Nested fields use double-underscore notation: `user__login`, not `user.login`.

**Slack messages:**
```sql
SELECT ts, user_id, text
FROM slack.messages(
    channel => 'C0B5LPBQSDR'
)
ORDER BY ts DESC
LIMIT 12
```

### Correlation engine

Four queries run in parallel — GitHub advisories, repo activity, `prod-incidents` channel, `security-alerts` channel. All results are concatenated into a single string and sent to the LLM.

The prompt asks three specific, falsifiable questions:
1. Did any merged PR precede an incident in Slack? (check timing, service name, error keywords)
2. Do any active advisories reference libraries or services in the GitHub/Slack feeds?
3. Are there repeated Slack patterns indicating systemic failure vs. one-off?

Required output format:

```
FINDING_1:
TYPE: (deploy-regression | advisory-match | slack-pattern | none)
CONFIDENCE: (low | medium | high)
CONFIDENCE_REASON: (one sentence — what evidence supports this)
TIMELINE: (what happened first, then what followed)
AFFECTED_SYSTEM: (service, repo, or component name)
BLAST_RADIUS: (what else could be affected)
RECOMMENDED_ACTION: (one concrete step the on-call engineer should take right now)
```

Findings are parsed back into Python dicts via regex and rendered as cards in the UI — color-coded by confidence, skipping any finding with `TYPE: none`.

```python
def parse_correlation_findings(raw_text):
    raw_text = raw_text.replace("**", "").replace("*", "").replace("#", "").replace("`", "")

    finding_blocks = re.findall(
        r"FINDING_\d+\s*[:\-]?\s*(.*?)(?=FINDING_\d+|OVERALL_VERDICT|$)",
        raw_text,
        re.DOTALL | re.IGNORECASE
    )
    ...
```

A second lighter AI call generates an executive summary with `THREAT_LEVEL`, `PRIMARY_CONCERN`, `IMPACT`, and `IMMEDIATE_ACTIONS` for non-technical stakeholders. All markdown is stripped from LLM output before rendering.

### Risk scoring

Deterministic keyword-based heuristic alongside the AI layer:

```python
def calculate_risk_score(incident_mentions, critical_count, high_count):
    score = (
        incident_mentions * 15
        + critical_count * 25
        + high_count * 12
    )
    return min(score, 100)
```

Feeds four header metrics: **Risk Index** (NOMINAL / ELEVATED / HIGH / CRITICAL), **Correlation Confidence**, **Active Signals**, **System Status**.

### Live clock (zero reruns)

The header clock runs in a JS iframe — not via `st_autorefresh`. Streamlit server is uninvolved after initial page load.

```python
components.html("""
<div id="live-clock" style="color:#E6C07B;font-size:38px;font-weight:800;">--:--:--</div>
<script>
function updateClock() {
    const now = new Date();
    document.getElementById('live-clock').textContent =
        String(now.getHours()).padStart(2,'0') + ':' +
        String(now.getMinutes()).padStart(2,'0') + ':' +
        String(now.getSeconds()).padStart(2,'0');
}
updateClock();
setInterval(updateClock, 1000);
</script>
""", height=140)
```

---

## Setup

### Prerequisites

- Python 3.9+
- [Coral CLI](https://withcoral.com/docs) installed and authenticated
- Groq API key
- Slack channel IDs for your workspace

### Install

```bash
git clone https://github.com/uk-repack/RasmalAI.git
cd RasmalAI
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key
```

Update `slack_channels` in the config with your channel IDs:

```python
slack_channels = {
    "prod-incidents": "C0B5LPBQSDR",
    "security-alerts": "C0B5WNUL6A0",
    "backend-team": "C0B5V016BT3"
}
```

### Run

```bash
streamlit run app.py
```

---

## Known Coral quirks

- `WHERE owner` and `WHERE repo` are required on all `github.*` queries. Missing them returns empty results, no error.
- Nested JSON fields use `__` separator: `user__login`, `pull_request__merged_at`.
- Slack queries use named parameter syntax: `slack.messages(channel => 'CHANNEL_ID')`.
- Archived or renamed Slack channels fail silently unless you surface `result.stderr`.

See [Coral Atlas](https://coral-atlas-query-ex-26t5.bolt.host/) for more documented quirks and working query examples.

---

## Limitations

Cross-source correlation currently relies on the LLM to join data that Coral returns as separate result sets. A native time-window JOIN in Coral would replace the fetch-stitch-correlate pipeline entirely:

```sql
SELECT p.title, p.merged_at, s.text, s.ts
FROM github.pulls p
JOIN slack.messages s
  ON s.ts BETWEEN p.merged_at AND p.merged_at + INTERVAL '2 hours'
  AND s.channel = 'prod-incidents'
WHERE p.repo = 'RasmalAI'
```

Risk scores are keyword heuristics, not statistical models. Treat them as glanceability indicators.

---

## Built at Coral Hackathon

72 hours. GitHub + Slack + Advisory feed → structured incident findings.

[Read the technical writeup](https://medium.com/@uk.ranjan101/how-i-built-rasmalai-a-real-time-incident-correlation-engine-on-top-of-coral-d6551cffa8e8)
