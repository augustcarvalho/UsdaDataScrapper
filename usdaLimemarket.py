# You will need to adjust the code in order to find the information you need depending on the page you are trying to get information from. In this case, the data is already clean and presented in a table format. I just wanted a quicker way of getting it updated everyday without having to open the website.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

today = datetime.datetime.now().strftime("%m/%d/%Y")  # get the current date in format MM/DD/YYYY

url = "https://marketnews.usda.gov/mnp/fv-report?commAbr=LIM&rowDisplayMax=100&locAbr=TX&repType=shipPriceDaily&locName=TEXAS&type=shipPrice&repTypeChanger=shipPriceDaily&startIndex=1&reportConfig=true&reportConfig=true&reportConfig=true&x=58&x=64&x=72&y=16&y=15&y=15&locChoose=locState&commodityClass=allcommodity&locAbrlength=1&locAbrPass=LIMES%7C%7CLIM&refine=false&step3date=true&repDate=" + today + "&endDate=" + today + "&organic=&environment=&_environment=1&Run=Run"

response = requests.get(url)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the HTML table using a more specific identifier (class)
    data_table = soup.find('table', class_='reportTable')

    if data_table:
        # Extract information from the specified <th> tag
        header_info = soup.find('th', colspan="14").text.strip()
        
        # Use pd.read_html to directly read the table into a DataFrame
        df_list = pd.read_html(str(data_table), header=2)
        
        # Select the DataFrame you need (based on your specific case)
        df_main = df_list[0]

        # Add a new row with header information
        header_row = pd.Series(['Header Information', header_info], index=['Date', 'Low-High Price'])
        df_header = pd.DataFrame([header_row])

        # Concatenate the main DataFrame and the header DataFrame
        df_combined = pd.concat([df_header, df_main], ignore_index=True)

        # Add a column for the current date
        df_combined['Date'] = today

        # Reorder columns (if needed)
        df_combined = df_combined[['Date', 'Low-High Price', 'Mostly Low-High Price', 'Season', 'Item Size']]

        # Save to Excel
        df_combined.to_excel(f'/Users/Documents/{today.replace("/", "_")}_prices.xlsx', index=False)
    else:
        print("Table not found on the page.")
else:
    print(f"Error: {response.status_code}")