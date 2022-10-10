import requests
from bs4 import BeautifulSoup
import pandas as pd

table_dictionary = pd.read_csv("tab_dictionary.csv")
month_dictionary = pd.read_csv("tab_month.csv")

dict = pd.Series(table_dictionary.table_name.values,
                 index=table_dictionary.index).to_dict()

dict_month = pd.Series(month_dictionary.month.values,
                 index=month_dictionary.index).to_dict()

str_tab = 0
url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type={0}&season=2022&month=0&season1=2022&ind=0'.format(str_tab)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

for tab in range (0,25):
    str_tab = str(tab)
    table1 = soup.find('table', id='LeaderBoard1_dg1_ctl00')
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)        
    df = pd.DataFrame(columns = headers)
    
    for month in range(1,7):
        month_number_page = month+3
        minIP = 0
        url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual={0}&type={1}&season=2022&month={2}&season1=2022&ind=0'.format(minIP, str_tab, month_number_page)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        div_pages = soup.find("div", {"class": "rgWrap rgInfoPart"})
        texts = [r.text.strip() for r in div_pages]
        pages = int(texts[3])
           
        table1 = soup.find('table', id='LeaderBoard1_dg1_ctl00')
        headers = []
        for i in table1.find_all('th'):
            title = i.text
            headers.append(title)  
        mydataComplete = pd.DataFrame(columns = headers)
    
        for page_number in range(0, pages):
            page_number_page = page_number+1
            url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual={0}&type={1}&season=2022&month={2}&season1=2022&ind=0&page={3}_30'.format(minIP, str_tab, month_number_page, page_number_page)
            
            # Create object page
            page = requests.get(url)
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
            mydata['MonthYear'] = ('2022-{0}-01').format(str(month_number_page))
            mydata['MonthYear']= pd.to_datetime(mydata['MonthYear'])
            frames = [mydataComplete, mydata]
            df_pages = pd.concat(frames)
            mydataComplete = df_pages           
        frames = [df, df_pages]
        df_months = pd.concat(frames)
        df = df_months     
    df_months=df_months.dropna(axis=1,how='all')
    df_months.to_csv('data/{0}/{0}_2022.csv'.format(dict.get(tab)), index=False)
    del df
    del df_months             