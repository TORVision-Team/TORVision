import os
from typing import Dict, Any
from google import genai

# Use the latest Gemini Flash-Lite model
MODEL_NAME = "models/gemini-flash-lite-latest"

def generate_incident_report(analysis_summary: Dict[str, Any]) -> str:
    """
    Generate a formal incident report from TORVision analysis
    using Google Gemini (AI Studio).
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

    # Initialize Gemini client with API key
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are assisting a law-enforcement cybercrime investigator.

Convert the following TOR network forensic analysis findings
into a professional INCIDENT REPORT.

Rules:
- Use formal, factual language
- Do NOT speculate beyond the data
- Do NOT claim TOR deanonymization
- Base conclusions only on metadata patterns

Incident Report Structure:
1. Executive Summary
2. Scope of Analysis
3. Key Observations
4. Risk Assessment
5. Recommended Next Steps

TORVision Analysis Findings:
{analysis_summary}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":
    # Example TORVision analysis summary
    sample_summary = {
        "time_range": "2025-02-01 to 2025-02-02",
        "total_tor_connections": 3421,
        "high_risk_nodes": 7,
        "risk_score_threshold": 0.85,
        "top_exit_countries": ["Germany", "Netherlands", "Russia"],
        "anomalies_detected": [
            "Repeated TOR circuit rebuilds",
            "High-frequency connections to a single exit node"
        ]
    }

    print("\n===== GENERATED INCIDENT REPORT =====\n")
    print(generate_incident_report(sample_summary))
