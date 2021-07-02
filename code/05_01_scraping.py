from bs4 import BeautifulSoup as Soup

table_html = """
<html>
  <table>
    <tr>
     <th>Name</th>
     <th>Date</th>
     <th>Team</th>
     <th>Opp</th>
     <th>Shots</th>
     <th>Goals</th>
    </tr>
    <tr>
     <th>Lionel Messi</th>
     <th>2018-06-16</th>
     <th>Argentina</th>
     <th>Iceland</th>
     <th>7</th>
     <th>0</th>
    </tr>
    <tr>
     <th>Luka Modric</th>
     <th>2018-06-21</th>
     <th>Croatia</th>
     <th>Argentina</th>
     <th>2</th>
     <th>1</th>
    </tr>
  </table>
<html>
"""

html_soup = Soup(table_html)

tr_tag = html_soup.find('tr')
tr_tag
type(tr_tag)

table_tag = html_soup.find('table')
type(table_tag)

td_tag = html_soup.find('td')
td_tag
type(td_tag)

td_tag
td_tag.string
str(td_tag.string)

tr_tag.find_all('th')

[str(x.string) for x in tr_tag.find_all('th')]

all_td_tags = table_tag.find_all('td')
all_td_tags

all_rows = table_tag.find_all('tr')
first_data_row = all_rows[1]  # 0 is header
first_data_row.find_all('td')

all_td_and_th_tags = table_tag.find_all(('td', 'th'))
all_td_and_th_tags

[str(x.string) for x in all_td_tags]

all_rows = table_tag.find_all('tr')
list_of_td_lists = [x.find_all('td') for x in all_rows[1:]]
list_of_td_lists
