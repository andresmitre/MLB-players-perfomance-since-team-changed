import requests
from bs4 import BeautifulSoup
import pandas as pd

table_dictionary = pd.read_csv("tab_dictionary.csv")
month_dictionary = pd.read_csv("tab_month.csv")

dict = pd.Series(table_dictionary.table_name.values,
                 index=table_dictionary.index).to_dict()

dict_month = pd.Series(month_dictionary.month.values,
                 index=month_dictionary.index).to_dict()

generic_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season=2022&month=0&season1=2022&ind=0'
page = requests.get(generic_url)
soup = BeautifulSoup(page.text, 'lxml')

for tab in range (1,24):
    str_tab = str(tab)
    div_pages = soup.find("div", {"class": "rgWrap rgInfoPart"})
    texts = [r.text.strip() for r in div_pages]
    pages = int(texts[3])
    # dictionary from 0-5
    for month in range(0,6):
        month_number_page = month+4
        for page_number in range(0, pages):
            page_number_page = page_number+1
            url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type={0}&season=2022&month={1}&season1=2022&ind=0&page={2}_30'.format(str_tab, month_number_page, page_number_page)
            
            # Create object page
            page = requests.get(url)

            # parser-lxml = Change html to Python friendly format
            # Obtain page's information
            soup = BeautifulSoup(page.text, 'lxml')

            table1 = soup.find('table', id='LeaderBoard1_dg1_ctl00')
            headers = []
            for i in table1.find_all('th'):
                title = i.text
                headers.append(title)
                
            mydata = pd.DataFrame(columns = headers)
            idx = 0
            for j in table1.find_all('tr')[1:]:
                row_data = j.find_all('td')
                row = [i.text for i in row_data]
                length = len(mydata)
                if idx<=1:
                    idx=idx+1
                    continue
                mydata.loc[length] = row
            mydata['MonthSeason'] = month+1
            mydata['MonthYear'] = month_number_page
            mydata.to_csv('data/{0}/{1}_Page_{2}.csv'.format(dict.get(tab), dict_month.get(month), page_number), index=False)