import requests
import json
import getpass
import re
import html
import pandas as pd
from datetime import datetime

# Allow HTTPS connections with self-signed cert
requests.packages.urllib3.disable_warnings()

# Create login session for Confluence
auth = ('mylogin', getpass.getpass())
s = requests.Session()
s.auth = auth
s.verify = False
s.headers = {"Content-Type": "application/json"}

# Confluence REST API URI
#WIKI = 'https://example.net/wiki/rest/api/'
WIKI = 'https://confluence.amd.com/display/DCGPUVAL/BKC+ROW+2.7.0'

# Obtain text from Confluence HTML layout
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    text = html.unescape(raw_html)
    text = re.sub(cleanr, '', text)
    text = text.replace(u'\xa0', u' ')
    return text

# Retrieving page data
def get_data(page_id):
    data = []
    r = s.get(
     '{}content/{}'.format(WIKI, page_id),
      params = dict(
       expand='body.view'
       )      
    )
    for content in r.json():
        pgdata = dict()
#I can't address to value as content['value']
        pgdata['text'] = cleanhtml(content['body']['view'].get('value'))
        data.append(pgdata)            
    return data

# Pages to extract from
with open(r'C:\\Users\\opena\\Documents\\pages.txt') as pagesf:
     pagesl = pagesf.read()
pages = pagesl.split(",\n")        
print(pages)

# Preparing data frame and exporting to Excel
textdata = list()
for page in pages:
    print('Handing:', page)
    textdata.extend(get_data(page))

df = pd.DataFrame(
    textdata, 
    columns = ['text']
)

df.to_excel('page_data{}.xlsx'.format(datetime.now().strftime("%Y_%m_%d_%H-%M")))