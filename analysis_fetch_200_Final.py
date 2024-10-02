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
("360 LIFE Inc", "360"),
("Betashares Australia 200 ETF", "A200"),
("The a2 Milk Company Ltd", "A2M"),
("Betashares Australian High Interest Cash ETF", "AAA"),
("Alcoa Corporation", "AAI"),
("Australian Foundation Investment Company Ltd", "AFI"),
("AGL Energy Ltd", "AGL"),
("Auckland International Airport Ltd", "AIA"),
("Ampol Ltd", "ALD"),
("Aristocrat Leisure Ltd", "ALL"),
("Als Ltd", "ALQ"),
("Atlas Arteria", "ALX"),
("Amcor Plc", "AMC"),
("AMP Ltd", "AMP"),
("Ansell Ltd", "ANN"),
("ANZ Group Holdings Ltd", "ANZ"),
("APA Group", "APA"),
("Eagers Automotive Ltd", "APE"),
("ARB Corporation Ltd", "ARB"),
("Argo Investments Ltd", "ARG"),
("ASX Ltd", "ASX"),
("AUB Group Ltd", "AUB"),
("Aurizon Holdings Ltd", "AZJ"),
("Bendigo and Adelaide Bank Ltd", "BEN"),
("BSP Financial Group Ltd", "BFL"),
("BHP Group Ltd", "BHP"),
("Brickworks Ltd", "BKW"),
("Bank of Queensland Ltd", "BOQ"),
("Beach Energy Ltd", "BPT"),
("Breville Group Ltd", "BRG"),
("Bluescope Steel Ltd", "BSL"),
("BWP Trust", "BWP"),
("Brambles Ltd", "BXB"),
("CAR Group Ltd", "CAR"),
("Commonwealth Bank of Australia", "CBA"),
("Codan Ltd", "CDA"),
("Challenger Ltd", "CGF"),
("Charter Hall Group", "CHC"),
("Champion Iron Ltd", "CIA"),
("Centuria Industrial REIT", "CIP"),
("Charter Hall Long Wale REIT", "CLW"),
("Capricorn Metals Ltd", "CMM"),
("Chorus Ltd", "CNU"),
("Cochlear Ltd", "COH"),
("Coles Group Ltd", "COL"),
("Computershare Ltd", "CPU"),
("Charter Hall Retail REIT", "CQR"),
("CSL Ltd", "CSL"),
("Clarity Pharmaceuticals Ltd", "CU6"),
("Cleanaway Waste Management Ltd", "CWY"),
("Dimensional Australian Core Equity Trust - Active ETF", "DACE"),
("De Grey Mining Ltd", "DEG"),
("Dimensional Global Core Equity Trust Aud Hedged - Active ETF", "DFGH"),
("Dimensional Global Core Equity Trust Unhedged - Active ETF", "DGCE"),
("Domino's PIZZA Enterprises Ltd", "DMP"),
("Downer Edi Ltd", "DOW"),
("Dexus", "DXS"),
("Ebos Group Ltd", "EBO"),
("Endeavour Group Ltd", "EDV"),
("Emerald Resources NL", "EMR"),
("Betashares Global Sustainability Leaders ETF", "ETHI"),
("Evolution Mining Ltd", "EVN"),
("Fletcher Building Ltd", "FBU"),
("Flight Centre Travel Group Ltd", "FLT"),
("Fortescue Ltd", "FMG"),
("Fisher & Paykel Healthcare Corporation Ltd", "FPH"),
("Genesis Minerals Ltd", "GMD"),
("Goodman Group", "GMG"),
("Graincorp Ltd", "GNC"),
("Genesis Energy Ltd", "GNE"),
("Global X Physical Gold", "GOLD"),
("Growthpoint Properties Australia", "GOZ"),
("GPT Group", "GPT"),
("GQG Partners Inc", "GQG"),
("Guzman Y GOMEZ Ltd", "GYG"),
("Betashares Active Australian Hybrids Fund (Managed Fund)", "HBRD"),
("Homeco Daily Needs REIT", "HDN"),
("HMC Capital Ltd", "HMC"),
("HUB24 Ltd", "HUB"),
("Harvey Norman Holdings Ltd", "HVN"),
("Hyperion GBL Growth Companies Fund (Managed Fund)", "HYGG"),
("Ishares Core Composite Bond ETF", "IAF"),
("Insurance Australia Group Ltd", "IAG"),
("Idp Education Ltd", "IEL"),
("Infratil Ltd", "IFT"),
("IGO Ltd", "IGO"),
("Iluka Resources Ltd", "ILU"),
("Ingenia Communities Group", "INA"),
("Ishares Global 100 ETF", "IOO"),
("Ishares Core S&P/ASX 200 ETF", "IOZ"),
("Incitec Pivot Ltd", "IPL"),
("Ishares S&P 500 ETF", "IVV"),
("JB Hi-Fi Ltd", "JBH"),
("James Hardie Industries Plc", "JHX"),
("Lendlease Group", "LLC"),
("Light & Wonder Inc", "LNW"),
("Lovisa Holdings Ltd", "LOV"),
("Lynas Rare EARTHS Ltd", "LYC"),
("Macquarie Technology Group Ltd", "MAQ"),
("Mercury NZ Ltd", "MCY"),
("Meridian Energy Ltd", "MEZ"),
("MFF Capital Investments Ltd", "MFF"),
("Magellan Global Fund (Open Class) (Managed Fund)", "MGOC"),
("Mirvac Group", "MGR"),
("Mineral Resources Ltd", "MIN"),
("Medibank Private Ltd", "MPL"),
("Macquarie Group Ltd", "MQG"),
("Metcash Ltd", "MTS"),
("Vaneck Australian EQUAL Weight ETF", "MVW"),
("Metrics Master Income Trust", "MXT"),
("National Australia Bank Ltd", "NAB"),
("National Australia Bank Ltd", "NABPH"),
("National Australia Bank Ltd", "NABPI"),
("Betashares Nasdaq 100 ETF", "NDQ"),
("Newmont Corporation", "NEM"),
("New Hope Corporation Ltd", "NHC"),
("Nib Holdings Ltd", "NHF"),
("Nickel Industries Ltd", "NIC"),
("National Storage REIT", "NSR"),
("Northern Star Resources Ltd", "NST"),
("Netwealth Group Ltd", "NWL"),
("NUIX Ltd", "NXL"),
("NEXTDC Ltd", "NXT"),
("Orora Ltd", "ORA"),
("Origin Energy Ltd", "ORG"),
("Orica Ltd", "ORI"),
("Paladin Energy Ltd", "PDN"),
("Pilbara Minerals Ltd", "PLS"),
("Pro Medicus Ltd", "PME"),
("Gold Corporation", "PMGOLD"),
("Premier Investments Ltd", "PMV"),
("Pinnacle Investment Management Group Ltd", "PNI"),
("Perpetual Ltd", "PPT"),
("Perseus Mining Ltd", "PRU"),
("PSC Insurance Group Ltd", "PSI"),
("Pexa Group Ltd", "PXA"),
("Qantas Airways Ltd", "QAN"),
("QBE Insurance Group Ltd", "QBE"),
("Vaneck MSCI International Quality ETF", "QUAL"),
("QUBE Holdings Ltd", "QUB"),
("REA Group Ltd", "REA"),
("RED 5 Ltd", "RED"),
("Reece Ltd", "REH"),
("Region Group", "RGN"),
("Ramsay Health Care Ltd", "RHC"),
("RIO Tinto Ltd", "RIO"),
("Resmed Inc", "RMD"),
("Ramelius Resources Ltd", "RMS"),
("Reliance Worldwide Corporation Ltd", "RWC"),
("SOUTH32 Ltd", "S32"),
("Scentre Group", "SCG"),
("Steadfast Group Ltd", "SDF"),
("Seek Ltd", "SEK"),
("Sandfire Resources Ltd", "SFR"),
("Sims Ltd", "SGM"),
("Stockland", "SGP"),
("Sonic Healthcare Ltd", "SHL"),
("Sigma Healthcare Ltd", "SIG"),
("Stanmore Resources Ltd", "SMR"),
("Summerset Group Holdings Ltd", "SNZ"),
("Washington H Soul Pattinson & Company Ltd", "SOL"),
("Spark New Zealand Ltd", "SPK"),
("Block Inc", "SQ2"),
("Santos Ltd", "STO"),
("SPDR S&P/ASX 200 Fund", "STW"),
("Super Retail Group Ltd", "SUL"),
("Suncorp Group Ltd", "SUN"),
("Seven Group Holdings Ltd", "SVW"),
("Transurban Group", "TCL"),
("The Lottery Corporation Ltd", "TLC"),
("Telstra Group Ltd", "TLS"),
("TELIX Pharmaceuticals Ltd", "TLX"),
("Technology One Ltd", "TNE"),
("TPG Telecom Ltd", "TPG"),
("Treasury Wine Estates Ltd", "TWE"),
("Vanguard Australian Fixed Interest INDEX ETF", "VAF"),
("Vanguard Australian Property Securities INDEX ETF", "VAP"),
("Vanguard Australian Shares INDEX ETF", "VAS"),
("Vicinity Centres", "VCX"),
("Vanguard Diversified High Growth INDEX ETF", "VDHG"),
("Viva Energy Group Ltd", "VEA"),
("Vanguard All-World Ex-US Shares INDEX ETF", "VEU"),
("Vanguard MSCI INDEX International Shares (Hedged) ETF", "VGAD"),
("Vanguard MSCI INDEX International Shares ETF", "VGS"),
("Vanguard Australian Shares High Yield ETF", "VHY"),
("Ventia Services Group Ltd", "VNT"),
("Vanguard US Total Market Shares INDEX ETF", "VTS"),
("Virgin Money Uk Plc", "VUK"),
("Westpac Banking Corporation", "WBC"),
("Woodside Energy Group Ltd", "WDS"),
("Webjet Ltd", "WEB"),
("Wesfarmers Ltd", "WES"),
("Westgold Resources Ltd", "WGX"),
("Whitehaven Coal Ltd", "WHC"),
("Worley Ltd", "WOR"),
("Woolworths Group Ltd", "WOW"),
("Wisetech Global Ltd", "WTC"),
("Xero Ltd", "XRO"),
("Yancoal Australia Ltd", "YAL"),
("ZIP Co Ltd", "ZIP")

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

        if any(keyword in line for keyword in keywords):
            for keyword in keywords:
                if keyword in line:
                    current_section = keyword
                    sections[current_section] += f'<h3>{current_section}</h3>\n'
                    break
        elif current_section:
            # Remove the ** formatting and add a single bullet point with a hyphen
            line = line.replace('**', '').strip()
            if ":" in line:
                title, content = line.split(":", 1)
                # Ensure no extra hyphen is added
                title = title.strip().lstrip('-')  # Remove any leading hyphen from the title
                sections[current_section] += f'<strong>- {title}:</strong>\n<p>{content.strip()}</p>\n'
            else:
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
