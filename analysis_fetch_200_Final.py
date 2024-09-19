import os
import requests
import time
from datetime import datetime
import pytz
import re

# Fetch the API key from environment variables
API_KEY = os.getenv('OPENAI')

# Output directory for HTML files (set to Premium by default)
output_dir = "Premium"

# List of 200 companies and their stock tickers
companies = [
    ("Ramsay Health Care Ltd", "RHC"),
    ("Wesfarmers Ltd", "WES"),
    # Add all other companies here
]

# Function to fetch analysis for a given company
def fetch_stock_analysis(stock, company_name):
    print(f"Fetching analysis for {company_name} ({stock})...")
    today = datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d')
    prompt = f"""Provide a detailed analysis of {company_name} ({stock}) as of today, {today}.

The response should be in Australian English. It should begin with the analysis and not state anything else, beginning with 'Current Performance'. The full analysis should state:

The analysis should cover the following areas:

Current Performance
• Revenue and Earnings Growth
• Profit Margins
• Earnings Per Share (EPS)
• Return on Equity (ROE)

Valuation Metrics
• Price-to-Earnings (P/E) Ratio
• P/E Ratio compared to the industry average

Analyst Recommendations
• Consensus Rating
• Price Targets

Insider Activity
• Recent Transactions
• Overall Sentiment

Dividend Analysis
• Dividend Yield
• Dividend Payout Ratio
• Dividend History

Market and Sector Conditions
• Relevant Sector Trends
• Economic Indicators
• Regulatory Environment

General Sentiment Analysis
• Media and News Sentiment
• Social Media and Public Sentiment
• Analyst Sentiment

Conclude with a summary paragraph that provides an overall assessment based on the analysis entitled 'Summary'.
There should be no sign off and do not include references."""

    headers = {
        'Authorization': f'Bearer {API_KEY}',  # The API key is injected here
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-4',  # Adjust the model as needed
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1500
    }

    for attempt in range(3):
        try:
            print("Sending request to OpenAI...")
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            print("Request sent, waiting for response...")
            response.raise_for_status()
            result = response.json()
            print("Request successful!")
            return result['choices'][0]['message']['content'].strip()
        except requests.RequestException as e:
            print(f"Error fetching analysis for {stock}: {e}")
            if response.status_code == 429:
                print("Rate limit hit. Waiting 60 seconds before retrying...")
                time.sleep(60)
            else:
                break
    return f"Failed to fetch analysis for {stock}."

# Function to parse the analysis text into structured sections with correct HTML formatting
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
                    if keyword != 'Summary':
                        sections[current_section] += f'<h3>{current_section}</h3>\n'
                    break
        elif current_section:
            sections[current_section] += f'<p>{line}</p>\n'

    return sections

# Function to save the analysis as an HTML file for each company with formatted sections
def save_analysis_as_html(content, company_name, stock):
    sections = parse_analysis(content)
    formatted_company_name = re.sub(r'[^a-zA-Z0-9]', '_', company_name.lower())
    filename = os.path.join(output_dir, f"{formatted_company_name}.html")
    
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
    with open(filename, "w") as f:
        f.write(formatted_content)
    print(f"Analysis for {company_name} ({stock}) saved to {filename}")

# Fetch, format, and save analysis for each company
for company_name, stock in companies:
    analysis = fetch_stock_analysis(stock, company_name)
    if not analysis.startswith("Failed"):
        save_analysis_as_html(analysis, company_name, stock)
    else:
        print(f"Skipping saving for {company_name} ({stock}) due to failed fetch.")
