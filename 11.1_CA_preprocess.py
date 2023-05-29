'''
Get report & county information, save those information to pickle
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pickle

# get all county
county_url='https://dq.cde.ca.gov/dataquest/page2.asp?level=County&subject=Enrollment&submit1=Submit'
response = requests.get(county_url)
soup = bs(response.text, 'html.parser')
cCountys=[]
for option in soup.find('select', {'name': 'cCounty'}).find_all('option'):
    text = option.text.strip().replace(' ','+')
    cCountys.append(text)


# step 1: get all 'Subject & topics' options (they are the same)
require_years=["2022-23","2021-22","2020-21","2019-20","2018-19","2017-18"]  #
level='County'

url = 'https://dq.cde.ca.gov/dataquest/'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
options = []
for select in soup.find_all('select'):
    for option in select.find_all('option'):
        label = option.get('label')
        content=option.text.strip()
        subject = option.get('value')
        try:
            step2='https://dq.cde.ca.gov/dataquest/page2.asp?level={}&subject={}&submit1=Submit'.format(level,subject)
            soup2 = bs(requests.get(step2).text, 'html.parser')
            rYears=[]
            for option in soup2.find('select', {'name': 'rYear'}).find_all('option'):
                text = option.get('value')
                rYears.append(text)
                
            intersection_set = set(require_years) & set(rYears)
            rYears = list(intersection_set)
            rYears.sort(reverse=True)
        except:
            rYears=''
        
        options.append({'label': label,'content': content, 'subject': subject,'exist_year':rYears})
df1 = pd.DataFrame(options)
df1 = df1.loc[df1['exist_year'].apply(lambda x: len(x) > 0),:]

# save data
data = (df1, cCountys)
bytes_data = pickle.dumps(data)
with open("CA_data/variables.pickle", "wb") as f:
    f.write(bytes_data)