# Will create tables that can be used to test the confluence updater program: confluence_table_updater.py
pip install -y atlassian-python-api

from atlassian import Confluence
import pandas as pd

df0 = pd.DataFrame({'Table': [1,2,3], 'Number': [4,5,6], 'One': [7,8,9]})
df1 = pd.DataFrame({'Table': [10,12,13], 'Number': [14,15,16], 'Two': [17,18,19]})

# convert to HTML
t0 = df0.to_html(index+False)
t1 = df1.to_html(index+False)

# combine the independent tables to add to a confluence page
df = t0 + t1

Function_Name = open('write_html.html','w')
Function_Name.write(df)
Function_Name.close()

################################################################################
# The above will create an html file
################################################################################

################################################################################
################################################################################

################################################################################
# This will create tables on a confluence page so the other program can be 
# executed against
################################################################################

conf_site  = 'https://confluence.com'
conf_user  = 'user'
conf_pass  = 'password'
conf_token = 'token_for_confluence'

page_title = 'Confluence Title'
page_space = 'Space Name'
page_id    = 'page_id_#'


####################################################################
# Atlassian Python API documentation
# https://atlassian-python-api.readthedocs.io/index.html
#
# Confluence:
# https://atlassian-python-api.readthedocs.io/confluence.html
####################################################################

# connect to Confluence
conf = Confluence(url=conf_site, username=conf_user, password=conf_pass, verify_ssl=False)
# if using a token instead of password, uncomment below and comment above line
#conf = Confluence(url=conf_site, username=conf_user, token=conf_token, verify_ssl=False)


# new page content
page_content = newHTML


# update page with new content
conf.update_page(page_id, page_title, page_content)
