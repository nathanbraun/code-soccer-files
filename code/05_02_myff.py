from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

response = requests.get('https://www.myfootballfacts.com/premier-league/all-time-premier-league/premier_league_goal_statistics/')

print(response.text)

soup = Soup(response.text)

# soup is a nested tag, so call find_all on it

tables = soup.find_all('table')

goals = tables[0]

# find_all always returns a list, even if there's only one element, which is
# the case here
len(tables)

# adp_table another nested tag, so call find_all again
rows = goals.find_all('tr')

# this is a header row
rows[2]

# data rows
first_data_row = rows[3]
first_data_row

rows = goals.find_all('tr')

# tds = adp_table.find_all('td')

# rows = []
# for i in range(len(tds)):
#     print(i)
#     if i % n == 0:
#         rows.append(tds[i:i+n])

# for i in range(0, len(tds), n):
#     print(i)

# n = 7
# tds2=[tds[i:i + n] for i in range(0, len(tds), n)]

# for i, td in enumerate(tds):

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[3:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df

# formatting
df = DataFrame(list_of_parsed_rows[:-2])

# clean up formatting
df.columns = ['season', 'matches', 'goals', 'gpm', 'max_score_team',
              'max_score_n', 'min_allow_team', 'min_allow_n',
              'max_allow_team', 'max_allow_n', 'min_score_team',
              'min_score_n']



df = df.apply(lambda x: x.str.replace(',',''))
float_cols = ['gpm']
int_cols = ['matches', 'goals', 'max_score_n', 'min_allow_n', 'max_allow_n',
           'min_score_n']

df[float_cols] = df[float_cols].astype(float)
df[int_cols] = df[int_cols].astype(int)

# done
df.head()

