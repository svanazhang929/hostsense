# HostSense — AI-Powered Host Retention Intelligence

An end-to-end agentic workflow that analyses 7,646 Airbnb hosts, identifies churn risk, and generates personalised AI retention strategies automatically.

## Live Demo
[hostsense-mrt7ntqipxtcrebrooztti.streamlit.app](https://hostsense-mrt7ntqipxtcrebrooztti.streamlit.app)

## How It Works
1. **Signal scoring** — Four behavioural signals (recency, frequency, availability, rating) produce a Churn Risk Score per host
2. **AI Agent 1** — Diagnoses churn reason and warning signals per high-risk host
3. **AI Agent 2** — Generates personalised retention strategy based on Agent 1's diagnosis
4. **Live dashboard** — Streamlit app surfaces risk distribution and AI analysis for the full host network

## Tech Stack
Python · SQL · SQLite · Claude API · Streamlit · Plotly · Inside Airbnb open data
