# 🏠 HostSense — AI-Powered Host Retention Intelligence

An end-to-end agentic workflow that analyses 7,646 Airbnb hosts, identifies churn risk, and generates personalised AI retention strategies automatically. A workflow that used to require hours of manual effort every week now runs in under 10 minutes.

**[Live Demo →](https://hostsense-mrt7ntqipxtcrebrooztti.streamlit.app)**

---

## The Problem

Airbnb hosts don't churn overnight. They disengage slowly — reviews dry up, calendars go dark, ratings slip. By the time a host success team notices, the window to intervene has already closed.

The manual process fails in four ways:
- Coverage is incomplete — only a fraction of hosts get reviewed each week
- It's reactive — churn is caught after it happens, not before
- Outreach is generic — one template sent to thousands of different situations
- It doesn't scale — more hosts means more headcount, not better systems

---

## The Solution

A three-layer agentic workflow that automates the entire process end-to-end.

**Layer 1 — Signal Detection (Python + SQL)**
Four behavioural signals scored per host: recency of last review, frequency drop, calendar pullback, and rating trajectory. Every host gets a Churn Risk Score from 0–100. 822 hosts flagged as high risk, representing $12.3M in estimated annual revenue.

**Layer 2 — AI Agent Diagnosis (Claude API)**
- Agent 1 analyses each high-risk host's signal profile and generates a specific churn diagnosis — primary reason, three warning signals, estimated timeline
- Agent 2 takes that diagnosis and produces a tailored retention strategy — immediate action, personalised offer, expected outcome
- Two agents run in sequence. The output of one becomes the context for the next.

**Layer 3 — Live Dashboard (Streamlit)**
Risk distribution across all 7,646 hosts, AI analysis per account, filterable by urgency and messaging tone. No manual reporting. Always on.

---

## Results

| | Before | After |
|---|---|---|
| Coverage | Sampled, incomplete | All 7,646 hosts |
| Time per cycle | 3–4 hours/week | Under 10 minutes |
| Retention strategy | Generic template | AI-personalised per host |
| Intervention timing | After churn | 3–6 months before |
| Revenue visibility | Partial | $12.3M quantified |

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data ingestion | Python, Pandas |
| Storage | SQLite, SQL |
| AI Agents | Claude API (claude-sonnet-4-5) |
| Dashboard | Streamlit, Plotly |
| Deployment | Streamlit Cloud |
| Data source | Inside Airbnb (Sydney, Sep 2025) |

---

## Project Structure
---

## Key Insights

1. **10.8% of Sydney hosts show critical disengagement signals** — zero availability, no reviews in over a year. They've already left. The platform just hasn't caught up yet.
2. **Churn is not a ratings problem.** The hosts most likely to churn are the ones who quietly stopped showing up — low availability, no recent reviews — regardless of their score.
3. **Sudden churn is more common than gradual fade.** A cluster of hosts went from active to fully disengaged in under 6 months. Early intervention on these accounts has the highest ROI.
