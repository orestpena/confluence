##################################################################
# This program will read in tables from a confluence page.
# A table can be modified or multiple tables modified.
# Then it updates each html for each table and then it can be 
# uploaded back to confluence.
##################################################################
pip install -y atlassian-python-api

from atlassian import Confluence
import panda as pd

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


# get current page content
page         = conf.get_page_by_id(page_id, expand='body.view')
page_content = page['body']['view']['value']
# depending on needs, may need to use storage in place of view. Reed documentation
# to determine needs.


# get table
# read_html documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_html.html
table        = pd.read_html(page_content)
table_length = len(table)


# add new column to the table
# assuming the confluence page has 2 tables on it, and a column will be added to the second
# table[0] and table[1]
table[1]['NEW'] = ''
# if there is only 1 table, then table['NEW'] = '' or table[0]['NEW'] = '' can be used


# convert table[s] to HTML
# to_html documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
newHTML = table[0].to_html(index=False)

if table_length > 1:
    for x in range(table_length-1):
        newHTML += table[x+1].to_html(index=False)


# new page content
page_content = newHTML


# update page with new content
conf.update_page(page_id, page_title, page_content)
