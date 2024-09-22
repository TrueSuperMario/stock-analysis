import os
import requests
import time
from datetime import datetime
import pytz
import re  # For replacing spaces and special characters

# Fetch the API key from environment variables
API_KEY = os.getenv('OPENAI')

# List of companies (shortened)
companies = [
    ("Ramsay Health Care Ltd", "RHC"),
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
    Conclude with a 'Summary' section.
    
    The format it should following is as per the below example you have previously produced:
    "Heading: Current Performance

    bullet point: Revenue and Earnings Growth:
    Mercury NZ has experienced a 5% year-on-year revenue growth, driven by higher electricity demand and increased production capacity from renewable sources. Earnings growth has been more modest at 3%, reflecting higher operational costs, particularly in infrastructure and network maintenance.

    bullet point: Profit Margins:
    The company’s net profit margin stands at 10%, which is relatively solid given the capital-intensive nature of the energy sector. While rising costs have impacted profitability slightly, Mercury’s focus on renewable energy helps sustain margins over the long term.

    bullet point: Earnings Per Share (EPS):
    EPS is currently at $0.72, representing a 2% increase from the previous year. This modest growth reflects Mercury’s steady performance in the renewable energy sector and its ability to maintain consistent profitability.

    bullet point: Return on Equity (ROE):
    Mercury’s ROE is 12%, indicating strong utilisation of shareholder equity to generate profits. This is considered healthy for a utility company, particularly one focused on renewable energy investments.

    Heading: Valuation Metrics

    bullet point: Price-to-Earnings (P/E) Ratio:
    The current P/E ratio for Mercury NZ is 19, suggesting the stock is moderately valued relative to its earnings potential. This valuation reflects the market’s confidence in the company’s renewable energy portfolio and stable cash flows.

    bullet point: P/E Ratio compared to the industry average:
    Mercury’s P/E ratio is slightly above the utilities industry average of 17, indicating a premium valuation driven by the company’s focus on sustainable energy and long-term growth prospects.

    Heading: Analyst Recommendations

    bullet point: Consensus Rating:
    Analysts have a 'Hold' consensus on Mercury NZ, noting the company’s stable performance and strong market position but also recognising limited short-term growth opportunities due to the mature state of the New Zealand energy market.

    bullet point: Price Targets:
    The average analyst price target is $6.50, with a range from $6.00 to $7.00. This suggests limited upside potential from current trading levels, reflecting expectations of steady but unspectacular growth.

    Heading: Insider Activity

    bullet point: Recent Transactions:
    Recent insider activity shows minor buying by executives, suggesting confidence in the company’s long-term strategy and future prospects. There has been no significant insider selling, which indicates stable sentiment among management.

    bullet point: Overall Sentiment:
    Insider sentiment remains neutral to positive, with recent transactions showing management's belief in Mercury’s ability to continue delivering stable returns to shareholders.

    Heading: Dividend Analysis

    bullet point: Dividend Yield:
    Mercury NZ offers a dividend yield of 4.2%, which is attractive for income-focused investors, particularly in the stable utilities sector. The yield is supported by the company’s consistent cash flows from renewable energy generation.

    bullet point: Dividend Payout Ratio:
    The payout ratio is 75%, indicating that Mercury returns a significant portion of its profits to shareholders while retaining enough capital for infrastructure investments and renewable energy projects.

    bullet point: Dividend History:
    Mercury has a solid history of dividend payments, with consistent distributions that have been gradually increased over time. This reflects the company’s strong cash flow and commitment to returning value to shareholders.

    heading: Market and Sector Conditions

    bullet point: Relevant Sector Trends:
    The renewable energy sector continues to experience growth, driven by increasing demand for clean energy and government incentives to reduce carbon emissions. Mercury is well-positioned within this sector, with its focus on hydroelectric, geothermal, and wind power.

    bullet point: Economic Indicators:
    Economic conditions remain supportive of the energy sector, with stable demand for electricity and ongoing investment in renewable infrastructure. However, inflationary pressures on costs and potential supply chain disruptions are key risks.

    bullet point: Regulatory Environment:
    The regulatory landscape for renewable energy remains favourable, with strong government support for the transition to sustainable energy. Mercury benefits from regulatory frameworks that incentivise renewable energy production and provide stability in electricity pricing.

    Heading: General Sentiment Analysis

    bullet point: Media and News Sentiment:
    Media coverage of Mercury NZ is generally positive, with a focus on its leadership in renewable energy generation and its ongoing investments in expanding its clean energy portfolio. The company’s commitment to sustainability is frequently highlighted as a key strength.

    bullet point: Social Media and Public Sentiment:
    Public sentiment on social media is largely favourable, with customers and stakeholders praising Mercury’s renewable energy efforts and reliability. There are occasional mentions of rising energy prices, but these concerns are typical across the sector.

    bullet point: Analyst Sentiment:
    Analyst sentiment is cautiously optimistic, reflecting confidence in Mercury’s long-term strategy and market position. However, some analysts remain cautious about the short-term impact of rising operational costs and the maturity of the New Zealand energy market.

    Heading: Summary:
    Mercury NZ Ltd is well-positioned in the renewable energy sector, benefiting from consistent revenue growth and a strong focus on sustainability. The company’s solid financial metrics, including a healthy ROE and attractive dividend yield, make it a reliable investment for income-focused investors. While the stock’s premium valuation reflects its renewable energy focus, analysts maintain a cautious outlook due to limited short-term growth opportunities and rising operational costs. Overall, Mercury’s commitment to clean energy and its stable market presence provide a solid foundation for long-term performance, making it an appealing option in the utilities sector."

This is exactly how it should be done every single time.
"""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-4o-mini',
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

        # Check for section headers (e.g., Current Performance, Valuation Metrics)
        if any(keyword in line for keyword in keywords):
            for keyword in keywords:
                if keyword in line:
                    current_section = keyword
                    sections[current_section] += f'<h3>{current_section}</h3>\n'
                    break
        elif current_section:
            # Replace **bold text** format with <strong>HTML tag</strong>
            line = line.replace('**', '').replace(':', ': <strong>')  # Replacing ** with <strong>
            
            # If line starts with a bullet point (e.g., "- **Strong Buy**: 5 analysts")
            if line.startswith("- "):
                sections[current_section] += f'<li>{line[2:]}</li>\n'  # Format as <li> without leading "- "
            else:
                sections[current_section] += f'<p>{line}</p>\n'

    # Wrap bullet points in <ul> tags for each section
    for section in sections:
        if '<li>' in sections[section]:
            sections[section] = f"<ul>\n{sections[section]}</ul>\n"

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
