import os
import requests
import time
from datetime import datetime
import pytz

# Create directories if they don't exist
os.makedirs('Basic', exist_ok=True)
os.makedirs('Basic Pro', exist_ok=True)
os.makedirs('Premium', exist_ok=True)

# Fetch the API key from environment variables
API_KEY = os.getenv('OPENAI')  # This will pull the 'OPENAI' secret

# List of 200 companies and their stock tickers
companies = [
    ("Ramsay Health Care Ltd", "RHC"),
    ("Wesfarmers Ltd", "WES"),
    ("Ampol Ltd", "ALD"),
    ("Dicker Data Ltd", "DDR"),
    ("CSL Ltd", "CSL"),
    ("Mineral Resources Ltd", "MIN"),
    ("Xero Ltd", "XRO"),
    ("ASX Ltd", "ASX"),
    ("Harvey Norman Holdings Ltd", "HVN"),
    ("Fortescue Ltd", "FMG"),
    ("Orica Ltd", "ORI"),
    ("Summerset Group Holdings Ltd", "SNZ"),
    ("Perpetual Ltd", "PPT"),
    ("AUB Group Ltd", "AUB"),
    ("Sonic Healthcare Ltd", "SHL"),
    ("ARB Corporation Ltd", "ARB"),
    ("Charter Hall Group", "CHC"),
    ("Spark New Zealand Ltd", "SPK"),
    ("Worley Ltd", "WOR"),
    ("Coles Group Ltd", "COL"),
    ("Challenger Ltd", "CGF"),
    ("Iress Ltd", "IRE"),
    ("Contact Energy Ltd", "CEN"),
    ("Perseus Mining Ltd", "PRU"),
    ("The a2 Milk Company Ltd", "A2M"),
    ("Woolworths Group Ltd", "WOW"),
    ("IPH Ltd", "IPH"),
    ("Mercury NZ Ltd", "MCY"),
    ("Nib Holdings Ltd", "NHF"),
    ("Graincorp Ltd", "GNC"),
    ("Seek Ltd", "SEK"),
    ("Polynovo Ltd", "PNV"),
    ("Domino's PIZZA Enterprises Ltd", "DMP"),
    ("Genesis Energy Ltd", "GNE"),
    ("Cleanaway Waste Management Ltd", "CWY"),
    ("Corporate Travel Management Ltd", "CTD"),
    ("Gold Road Resources Ltd", "GOR"),
    ("Medibank Private Ltd", "MPL"),
    ("Metcash Ltd", "MTS"),
    ("BWP Trust", "BWP"),
    ("Bellevue Gold Ltd", "BGL"),
    ("Ebos Group Ltd", "EBO"),
    ("Metrics Master Income Trust", "MXT"),
    ("Viva Energy Group Ltd", "VEA"),
    ("WAM Capital Ltd", "WAM"),
    ("Air New Zealand Ltd", "AIZ"),
    ("Wam Leaders Ltd", "WLE"),
    ("Origin Energy Ltd", "ORG"),
    ("MFF Capital Investments Ltd", "MFF"),
    ("Australian Foundation Investment Company Ltd", "AFI"),
    ("PSC Insurance Group Ltd", "PSI"),
    ("Waypoint REIT", "WPR"),
    ("Aurizon Holdings Ltd", "AZJ"),
    ("Nine Entertainment Co. Holdings Ltd", "NEC"),
    ("NUIX Ltd", "NXL"),
    ("Orora Ltd", "ORA"),
    ("Nickel Industries Ltd", "NIC"),
    ("Homeco Daily Needs REIT", "HDN"),
    ("NRW Holdings Ltd", "NWH"),
    ("CAR Group Ltd", "CAR"),
    ("Virgin Money Uk Plc", "VUK"),
    ("AMP Ltd", "AMP"),
    ("Deterra Royalties Ltd", "DRR"),
    ("West African Resources Ltd", "WAF"),
    ("De Grey Mining Ltd", "DEG"),
    ("Sigma Healthcare Ltd", "SIG"),
    ("Guzman Y GOMEZ Ltd", "GYG"),
    ("Ramelius Resources Ltd", "RMS"),
    ("Vicinity Centres", "VCX"),
    ("RED 5 Ltd", "RED"),
    ("GQG Partners Inc", "GQG"),
    ("Region Group", "RGN"),
    ("Incitec Pivot Ltd", "IPL"),
    ("Mirvac Group", "MGR"),
    ("Coronado Global Resources Inc", "CRN"),
    ("National Storage REIT", "NSR"),
    ("Telstra Group Ltd", "TLS"),
    ("APA Group", "APA"),
    ("Liontown Resources Ltd", "LTR"),
    ("Beach Energy Ltd", "BPT"),
    ("Endeavour Group Ltd", "EDV"),
    ("New Hope Corporation Ltd", "NHC"),
    ("Scentre Group", "SCG"),
    ("Abacus Storage King", "ASK"),
    ("Lynas Rare EARTHS Ltd", "LYC"),
    ("Paladin Energy Ltd", "PDN"),
    ("QUBE Holdings Ltd", "QUB"),
    ("Bapcor Ltd", "BAP"),
    ("Atlas Arteria", "ALX"),
    ("Stanmore Resources Ltd", "SMR"),
    ("Growthpoint Properties Australia", "GOZ"),
    ("Evolution Mining Ltd", "EVN"),
    ("SOUTH32 Ltd", "S32"),
    ("Judo Capital Holdings Ltd", "JDO"),
    ("Charter Hall Long Wale REIT", "CLW"),
    ("Webjet Ltd", "WEB"),
    ("Treasury Wine Estates Ltd", "TWE"),
    ("Chorus Ltd", "CNU"),
    ("The Lottery Corporation Ltd", "TLC"),
    ("Bank of Queensland Ltd", "BOQ"),
    ("GPT Group", "GPT"),
    ("Ventia Services Group Ltd", "VNT"),
    ("L1 Long Short Fund Ltd", "LSF"),
    ("Centuria Industrial REIT", "CIP"),
    ("Santos Ltd", "STO"),
    ("Pilbara Minerals Ltd", "PLS"),
    ("Argo Investments Ltd", "ARG"),
    ("Stockland", "SGP"),
    ("Arena REIT", "ARF"),
    ("Charter Hall Retail REIT", "CQR"),
    ("Reliance Worldwide Corporation Ltd", "RWC"),
    ("Domain Holdings Australia Ltd", "DHG"),
    ("Bluescope Steel Ltd", "BSL"),
    ("Whitehaven Coal Ltd", "WHC"),
    ("Sandfire Resources Ltd", "SFR"),
    ("Meridian Energy Ltd", "MEZ"),
    ("QBE Insurance Group Ltd", "QBE"),
    ("Auckland International Airport Ltd", "AIA"),
    ("Lovisa Holdings Ltd", "LOV"),
    ("Emerald Resources NL", "EMR"),
    ("Ingenia Communities Group", "INA"),
    ("Insurance Australia Group Ltd", "IAG"),
    ("Zimplats Holdings Ltd", "ZIM"),
    ("James Hardie Industries Plc", "JHX"),
    ("Steadfast Group Ltd", "SDF"),
    ("Resmed Inc", "RMD"),
    ("ZIP Co Ltd", "ZIP"),
    ("Lendlease Group", "LLC"),
    ("HMC Capital Ltd", "HMC"),
    ("Genesis Minerals Ltd", "GMD"),
    ("Iluka Resources Ltd", "ILU"),
    ("Infratil Ltd", "IFT"),
    ("Computershare Ltd", "CPU"),
    ("Dexus", "DXS"),
    ("TELIX Pharmaceuticals Ltd", "TLX"),
    ("Yancoal Australia Ltd", "YAL"),
    ("Amcor Plc", "AMC"),
    ("Tuas Ltd", "TUA"),
    ("NEXTDC Ltd", "NXT"),
    ("Sims Ltd", "SGM"),
    ("Capricorn Metals Ltd", "CMM"),
    ("Champion Iron Ltd", "CIA"),
    ("Als Ltd", "ALQ"),
    ("Transurban Group", "TCL"),
    ("Spartan Resources Ltd", "SPR"),
    ("LIFE360 Inc", "360"),
    ("Westgold Resources Ltd", "WGX"),
    ("Westpac Banking Corporation", "WBC"),
    ("Washington H Soul Pattinson & Company Ltd", "SOL"),
    ("Brickworks Ltd", "BKW"),
    ("Technology One Ltd", "TNE"),
    ("Idp Education Ltd", "IEL"),
    ("Wisetech Global Ltd", "WTC"),
    ("Fletcher Building Ltd", "FBU"),
    ("Suncorp Group Ltd", "SUN"),
    ("Super Retail Group Ltd", "SUL"),
    ("Bendigo and Adelaide Bank Ltd", "BEN"),
    ("Ansell Ltd", "ANN"),
    ("National Australia Bank Ltd", "NAB"),
    ("IGO Ltd", "IGO"),
    ("Codan Ltd", "CDA"),
    ("BHP Group Ltd", "BHP"),
    ("AGL Energy Ltd", "AGL"),
    ("Northern Star Resources Ltd", "NST"),
    ("BSP Financial Group Ltd", "BFL"),
    ("Eagers Automotive Ltd", "APE"),
    ("Breville Group Ltd", "BRG"),
    ("Goodman Group", "GMG"),
    ("Netwealth Group Ltd", "NWL"),
    ("Premier Investments Ltd", "PMV"),
    ("EVT Ltd", "EVT"),
    ("Pinnacle Investment Management Group Ltd", "PNI"),
    ("Qantas Airways Ltd", "QAN"),
    ("Fisher & Paykel Healthcare Corporation Ltd", "FPH"),
    ("ANZ Group Holdings Ltd", "ANZ"),
    ("Magellan Financial Group Ltd", "MFG"),
    ("Neuren Pharmaceuticals Ltd", "NEU"),
    ("TPG Telecom Ltd", "TPG"),
    ("Pexa Group Ltd", "PXA"),
    ("Brambles Ltd", "BXB"),
    ("Alcoa Corporation", "AAI"),
    ("Flight Centre Travel Group Ltd", "FLT"),
    ("Woodside Energy Group Ltd", "WDS"),
    ("Seven Group Holdings Ltd", "SVW"),
    ("Clarity Pharmaceuticals Ltd", "CU6"),
    ("Reece Ltd", "REH"),
    ("Aristocrat Leisure Ltd", "ALL"),
    ("Commonwealth Bank of Australia", "CBA"),
    ("REA Group Ltd", "REA"),
    ("Downer Edi Ltd", "DOW"),
    ("Macquarie Group Ltd", "MQG"),
    ("HUB24 Ltd", "HUB"),
    ("JB Hi-Fi Ltd", "JBH"),
    ("RIO Tinto Ltd", "RIO"),
    ("Newmont Corporation", "NEM"),
    ("Light & Wonder Inc", "LNW"),
    ("Macquarie Technology Group Ltd", "MAQ"),
    ("Block Inc", "SQ2"),
    ("Pro Medicus Ltd", "PME"),
    ("Cochlear Ltd", "COH")
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
        'model': 'gpt-4o-mini',  # Model specified by you
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
    # Define sections with initial empty strings
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

    # Define keywords to split the sections based on the structure provided
    keywords = list(sections.keys())
    current_section = None

    # Split the text by sections and format appropriately
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Check if the line starts with a section header
        if any(keyword in line for keyword in keywords):
            for keyword in keywords:
                if keyword in line:
                    current_section = keyword
                    if keyword != 'Summary':  # Avoid adding duplicate 'Summary' heading
                        sections[current_section] += f'<h3>{current_section}</h3>\n'  # Add section header
                    break
        elif current_section:
            # Check if the line is a bullet point formatted with "- **Title**:"
            if line.startswith('**') and line.endswith('**'):
                bullet_title = line.strip('**')
                sections[current_section] += f'<h4>{bullet_title}</h4>\n'  # Format bullet point as <h4>
            elif line.startswith('**') and ':' in line:
                bullet_title, bullet_content = line.split(':', 1)
                sections[current_section] += f'<h4>{bullet_title.strip("**").strip()}</h4>\n<p>{bullet_content.strip()}</p>\n'
            else:
                sections[current_section] += f'<p>{line}</p>\n'  # For regular paragraph content

    return sections

import re  # Import re for replacing spaces and special characters

# Function to save the analysis as an HTML file for each company with formatted sections
def save_analysis_as_html(content, company_name, stock):
    sections = parse_analysis(content)
    
    # Format the company name to be used in the filename: lowercase, replace spaces with underscores, and remove special characters
    formatted_company_name = re.sub(r'[^a-zA-Z0-9]', '_', company_name.lower())

    # Set the filename to be the formatted company name
    filename = f"{formatted_company_name}.html"  # Append date to filename
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
    {sections['Summary']}  <!-- Relying on the parsed content to add the Summary heading if needed -->

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
