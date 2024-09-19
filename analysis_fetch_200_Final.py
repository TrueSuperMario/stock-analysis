import os
import requests
import time
from datetime import datetime
import pytz
import re  # For replacing spaces and special characters

# Fetch the API key from environment variables
API_KEY = os.getenv('OPENAI')

# List of 200 companies and their stock tickers
companies = [
    ("Ramsay Health Care Ltd", "RHC"),
    ("Wesfarmers Ltd", "WES"),
    # Add remaining companies
]

# Function to fetch analysis for a given company
def fetch_stock_analysis(stock, company_name):
    print(f"Fetching analysis for {company_name} ({stock})...")
    today = datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d')
    prompt = f"""Provide a detailed analysis of {company_name} ({stock}) as of today, {today}.
    The analysis should cover the following areas:
    - Current Performance
    - Valuation Metrics
    - Analyst Recommendations
    - Insider Activity
    - Dividend Analysis
    - Market and Sector Conditions
    - General Sentiment Analysis
    Conclude with a 'Summary' section."""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-4o-mini',  # Model specified by you
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1500
    }

    for attempt in range(3):
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.RequestException as e:
            print(f"Error fetching analysis for {stock}: {e}")
            if response.status_code == 429:
                time.sleep(60)
            else:
                break
    return f"Failed to fetch analysis for {stock}."

# Function to parse the analysis text into structured sections
def parse_analysis(text):
    sections = {
        'Current Performance': '',
        'Valuation Metrics': '',
        'Analyst Recommendations': '',
        'Insider Activity': '',
        'Dividend Analysis': '',
        'Market and Sector Conditions': '',
        'General Sentiment Analysis': '',
        'Summary': ''
    }

    keywords = list(sections.keys())
    current_section = None

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue

        if any(keyword in line for keyword in keywords):
            for keyword in keywords:
                if keyword in line:
                    current_section = keyword
                    sections[current_section] += f'<h3>{current_section}</h3>\n'
                    break
        elif current_section:
            sections[current_section] += f'<p>{line}</p>\n'

    return sections

# Function to save the analysis as an HTML file
def save_analysis_as_html(content, company_name, stock):
    sections = parse_analysis(content)
    formatted_company_name = re.sub(r'[^a-zA-Z0-9]', '_', company_name.lower())
    filename = f"Premium/{formatted_company_name}.html"  # Save to 'Premium' folder
    formatted_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} ({stock}) Analysis</title>
</head>
<body>
    {sections['Current Performance']}
    {sections['Valuation Metrics']}
    {sections['Analyst Recommendations']}
    {sections['Insider Activity']}
    {sections['Dividend Analysis']}
    {sections['Market and Sector Conditions']}
    {sections['General Sentiment Analysis']}
    {sections['Summary']}
</body>
</html>
"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
    with open(filename, "w") as f:
        f.write(formatted_content)
    print(f"Analysis for {company_name} ({stock}) saved to {filename}")

# Main loop to fetch and save analysis for each company
for company_name, stock in companies:
    analysis = fetch_stock_analysis(stock, company_name)
    if not analysis.startswith("Failed"):
        save_analysis_as_html(analysis, company_name, stock)
    else:
        print(f"Skipping saving for {company_name} ({stock}) due to failed fetch.")
