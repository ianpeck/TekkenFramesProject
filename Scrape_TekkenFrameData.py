# --- Imports --- #

from bs4 import BeautifulSoup
import requests
import pandas as pd

# --- Get Links --- #

mainurl = 'http://rbnorway.org/t7-frame-data/'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

fighterhtml = requests.get(mainurl, headers=headers).text

soup2 = BeautifulSoup(fighterhtml, "lxml")

fighter_linkparts = set()

for link in soup2.find_all("a"):
    if '-t7-frames' in "href: {}".format(link.get("href")):
        fighter_linkparts.add("href: {}".format(link.get("href")).replace('href: ','').replace('http://rbnorway.org/', '').replace('/',''))

fighter_linkparts = sorted(fighter_linkparts)

# --- BeautifulSoup Loop Initialization / Data Wrangling --- #
No_More_headings = False
headings = []
df = pd.DataFrame()

for fighter in fighter_linkparts:

    # Set Up Variables for Each Fighter
    url = 'http://rbnorway.org/{}/'.format(fighter)
    html_content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_content, "lxml")

    try:
        special_table = soup.find('div', id='special').find_next_sibling('table')
        basic_table = soup.find('div', id='basic').find_next_sibling('table')
    except AttributeError:
        pass

    frame_tables = []

    try:
        frame_tables.append(special_table)
        frame_tables.append(basic_table)
    except NameError:
        pass

    table_data = []

# Get Headers/Data
    for table in frame_tables:
        while No_More_headings is False:
            for th in table.thead.find("tr"):
                if th != '\n' and th.text not in headings:
                    headings.append(th.text)  # removes tags
            No_More_headings = True
        for td in table.tbody.findAll("tr"):  # only grabs 8 good columns, skips others
            new_row = td.text.split('\n')
            new_row = new_row[1:9]
            table_data.append(new_row)

    # Remove Blank Entries in Data / Append Character Name
    for rows in table_data:
        rows.append(fighter.replace('-t7-frames','').replace('-', ' ').title())
    # Append Data
    df = df.append(table_data)

# --- Sets up/Pushes Dataframe to CSV for checking ---

headings.append('Character')
df.columns = headings
df.to_csv('/Users/ianjpeck/Documents/tekken.csv', index = False)








