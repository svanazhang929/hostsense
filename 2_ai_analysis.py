import sqlite3
import pandas as pd
import anthropic
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=== AI Analysis: Airbnb Host Churn ===\n")

conn = sqlite3.connect('airbnb_churn.db')

high_risk = pd.read_sql("""
    SELECT 
        host_id, host_name, total_listings, avg_churn_score,
        avg_rating, total_reviews_ltm, avg_availability,
        days_since_last_review, estimated_revenue, risk_tier
    FROM host_stats
    WHERE risk_tier = 'High'
    ORDER BY avg_churn_score DESC
    LIMIT 20
""", conn)

print(f"Analysing top {len(high_risk)} high-risk hosts...\n")

def analyse_churn_reason(host):
    prompt = f"""You are an Airbnb platform analyst. Based on this host data, identify why they may be churning.
IMPORTANT: Respond in English only. Do not use any other language.

Host Data:
- Name: {host['host_name']}
- Churn Risk Score: {host['avg_churn_score']}/100
- Rating: {host['avg_rating']:.2f}/5.0
- Days Since Last Review: {int(host['days_since_last_review'])}
- Reviews Last 12 Months: {int(host['total_reviews_ltm'])}
- Availability days/year: {int(host['avg_availability'])}
- Estimated Annual Revenue: ${host['estimated_revenue']:,.0f}

Respond ONLY with valid JSON, no markdown, no explanation:
{{"primary_reason": "one sentence in English", "signal_1": "first warning signal in English", "signal_2": "second warning signal in English", "signal_3": "third warning signal in English", "churn_probability": "High or Very High or Critical", "time_to_churn": "e.g. 1-3 months"}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def generate_retention_strategy(host, churn):
    prompt = f"""You are an Airbnb host success manager. Generate a retention strategy for this at-risk host.
IMPORTANT: Respond in English only. Do not use any other language.

Host Profile:
- Churn Risk Score: {host['avg_churn_score']}/100
- Primary Reason: {churn['primary_reason']}
- Revenue at Risk: ${host['estimated_revenue']:,.0f}/year
- Days Inactive: {int(host['days_since_last_review'])}

Respond ONLY with valid JSON, no markdown, no explanation:
{{"immediate_action": "one specific action within 24 hours in English", "retention_offer": "specific incentive to offer in English", "messaging_tone": "Urgent or Supportive or Informational", "expected_outcome": "what success looks like in English", "priority_score": 8}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


results = []

for i, (_, host) in enumerate(high_risk.iterrows()):
    print(f"[{i+1}/{len(high_risk)}] Analysing {host['host_name']}...")
    try:
        churn = analyse_churn_reason(host)
        retention = generate_retention_strategy(host, churn)

        results.append({
            'host_id': int(host['host_id']),
            'host_name': str(host['host_name']),
            'churn_risk_score': float(host['avg_churn_score']),
            'avg_rating': float(host['avg_rating']),
            'days_since_last_review': int(host['days_since_last_review']),
            'estimated_revenue': float(host['estimated_revenue']),
            'primary_reason': str(churn.get('primary_reason', '')),
            'signal_1': str(churn.get('signal_1', '')),
            'signal_2': str(churn.get('signal_2', '')),
            'signal_3': str(churn.get('signal_3', '')),
            'churn_probability': str(churn.get('churn_probability', '')),
            'time_to_churn': str(churn.get('time_to_churn', '')),
            'immediate_action': str(retention.get('immediate_action', '')),
            'retention_offer': str(retention.get('retention_offer', '')),
            'messaging_tone': str(retention.get('messaging_tone', '')),
            'expected_outcome': str(retention.get('expected_outcome', '')),
            'priority_score': int(retention.get('priority_score', 5))
        })
        time.sleep(0.5)

    except Exception as e:
        print(f"  Error: {e}")
        continue

results_df = pd.DataFrame(results)

conn.execute("DROP TABLE IF EXISTS ai_analysis")
conn.execute("""
    CREATE TABLE ai_analysis (
        host_id INTEGER, host_name TEXT, churn_risk_score REAL,
        avg_rating REAL, days_since_last_review INTEGER,
        estimated_revenue REAL, primary_reason TEXT,
        signal_1 TEXT, signal_2 TEXT, signal_3 TEXT,
        churn_probability TEXT, time_to_churn TEXT,
        immediate_action TEXT, retention_offer TEXT,
        messaging_tone TEXT, expected_outcome TEXT,
        priority_score INTEGER
    )
""")
conn.commit()

for _, row in results_df.iterrows():
    conn.execute("INSERT INTO ai_analysis VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(row))
conn.commit()

print(f"\n✅ AI analysis complete: {len(results_df)} hosts analysed")
print("\nSample results:")
print(results_df[['host_name','churn_risk_score','primary_reason','immediate_action']].head(3).to_string(index=False))

conn.close()
print("\n✅ Results saved to airbnb_churn.db -> table: ai_analysis")
