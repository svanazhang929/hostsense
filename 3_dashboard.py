import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="HostSense — Airbnb Churn Intelligence",
    page_icon="🏠",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('airbnb_churn.db')
    host_stats = pd.read_sql("SELECT * FROM host_stats", conn)
    ai_analysis = pd.read_sql("SELECT * FROM ai_analysis", conn)
    conn.close()
    return host_stats, ai_analysis

host_stats, ai_analysis = load_data()

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🏠 HostSense")
st.markdown("### AI-Powered Host Retention Intelligence for Airbnb")
st.markdown("---")

# ── KPI Row ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_hosts = len(host_stats)
high_risk = len(host_stats[host_stats['risk_tier'] == 'High'])
medium_risk = len(host_stats[host_stats['risk_tier'] == 'Medium'])
revenue_at_risk = len(host_stats[host_stats['risk_tier'] == 'High']) * 15000
col1.metric("Total Hosts", f"{total_hosts:,}")
col2.metric("🔴 High Risk", f"{high_risk:,}", f"{high_risk/total_hosts*100:.1f}% of hosts")
col3.metric("🟡 Medium Risk", f"{medium_risk:,}", f"{medium_risk/total_hosts*100:.1f}% of hosts")
col4.metric("💰 Revenue at Risk", f"${revenue_at_risk/1e6:.1f}M", "High risk hosts")

st.markdown("---")

# ── AS-IS vs TO-BE ───────────────────────────────────────────────────────────
st.markdown("## The Problem This Solves")

col_left, col_right = st.columns(2)

with col_left:
    st.error("""
    **❌ AS-IS: Manual Process**
    
    - Host success team manually reviews host accounts
    - No systematic way to identify who's at risk
    - By the time churn is noticed, host has already left
    - Generic re-engagement emails sent to everyone
    - **Time per analysis: 3–4 hours/week**
    - **Result: Reactive, too late, not scalable**
    """)

with col_right:
    st.success("""
    **✅ TO-BE: AI-Automated Workflow**
    
    - Automated churn risk scoring across all 7,646 hosts
    - AI identifies at-risk hosts before they disengage
    - Personalised retention strategies per host
    - Priority queue for host success team
    - **Time per analysis: < 10 minutes**
    - **Result: Proactive, personalised, scalable**
    """)

st.markdown("---")

# ── Risk Distribution ────────────────────────────────────────────────────────
st.markdown("## Risk Distribution Across Sydney Hosts")

col1, col2 = st.columns(2)

with col1:
    risk_counts = host_stats['risk_tier'].value_counts().reset_index()
    risk_counts.columns = ['Risk Tier', 'Count']
    color_map = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#22c55e'}
    fig_pie = px.pie(
        risk_counts, values='Count', names='Risk Tier',
        color='Risk Tier', color_discrete_map=color_map,
        title='Host Risk Distribution'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_hist = px.histogram(
        host_stats, x='avg_churn_score', nbins=40,
        color_discrete_sequence=['#6366f1'],
        title='Churn Risk Score Distribution',
        labels={'avg_churn_score': 'Churn Risk Score (0-100)'}
    )
    fig_hist.add_vline(x=65, line_dash="dash", line_color="red", annotation_text="High Risk threshold")
    fig_hist.add_vline(x=40, line_dash="dash", line_color="orange", annotation_text="Medium Risk threshold")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# ── AI Analysis Results ──────────────────────────────────────────────────────
st.markdown("## 🤖 AI Agent Analysis — Top High-Risk Hosts")
st.markdown("*Agent 1 identifies churn reasons · Agent 2 generates personalised retention strategies*")

if len(ai_analysis) > 0:
    # Priority filter
    tone_filter = st.selectbox(
        "Filter by messaging tone:",
        ["All"] + list(ai_analysis['messaging_tone'].unique())
    )

    filtered = ai_analysis if tone_filter == "All" else ai_analysis[ai_analysis['messaging_tone'] == tone_filter]

    for _, row in filtered.iterrows():
        risk_color = "🔴" if row['churn_risk_score'] >= 75 else "🟡"

        with st.expander(f"{risk_color} **{row['host_name']}** — Risk Score: {row['churn_risk_score']:.0f}/100 · Priority: {row['priority_score']}/10"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Churn Risk Score", f"{row['churn_risk_score']:.0f}/100")
            col2.metric("Days Inactive", f"{int(row['days_since_last_review'])} days")
            col3.metric("Revenue at Risk", f"${row['estimated_revenue']:,.0f}")

            st.markdown("**🔍 Agent 1: Churn Analysis**")
            st.warning(f"**Primary Reason:** {row['primary_reason']}")
            st.markdown(f"- ⚠️ {row['signal_1']}")
            st.markdown(f"- ⚠️ {row['signal_2']}")
            st.markdown(f"- ⚠️ {row['signal_3']}")
            st.markdown(f"**Churn Probability:** {row['churn_probability']} · **Estimated Timeline:** {row['time_to_churn']}")

            st.markdown("**💡 Agent 2: Retention Strategy**")
            st.info(f"**Immediate Action (24hrs):** {row['immediate_action']}")
            st.success(f"**Retention Offer:** {row['retention_offer']}")
            st.markdown(f"**Messaging Tone:** {row['messaging_tone']} · **Expected Outcome:** {row['expected_outcome']}")
else:
    st.warning("No AI analysis data found. Run 2_ai_analysis.py first.")

st.markdown("---")

# ── Churn Score Breakdown ────────────────────────────────────────────────────
st.markdown("## 📊 What Drives Churn Risk?")
st.markdown("Each host's risk score is built from four signals:")

col1, col2 = st.columns(2)

with col1:
    # Scatter: Days Inactive vs Churn Score, colored by risk tier
    color_map = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#22c55e'}
    fig_scatter = px.scatter(
        host_stats,
        x='days_since_last_review',
        y='avg_churn_score',
        color='risk_tier',
        color_discrete_map=color_map,
        opacity=0.5,
        title='Days Inactive vs Churn Risk Score',
        labels={
            'days_since_last_review': 'Days Since Last Review',
            'avg_churn_score': 'Churn Risk Score',
            'risk_tier': 'Risk Tier'
        }
    )
    fig_scatter.add_hline(y=65, line_dash="dash", line_color="red", annotation_text="High Risk")
    fig_scatter.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Medium Risk")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    top20 = host_stats.nlargest(20, 'avg_churn_score')
    fig_bar = px.bar(
        top20, x='avg_churn_score', y='host_name',
        orientation='h', color='avg_churn_score',
        color_continuous_scale='Reds',
        title='Top 20 Highest Risk Hosts',
        labels={'avg_churn_score': 'Churn Risk Score', 'host_name': 'Host'}
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85em;'>
HostSense · Built with Python, SQLite, Claude API & Streamlit · 
Data: Inside Airbnb Sydney (Sep 2025) · 15,020 listings · 7,646 hosts
</div>
""", unsafe_allow_html=True)