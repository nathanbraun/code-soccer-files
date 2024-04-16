from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

response = requests.get('https://www.worldfootball.net/schedule/eng-premier-league-2022-2023-spieltag/38/')

print(response.text)

soup = Soup(response.text)

# soup is a nested tag, so call find_all on it

tables = soup.find_all('table')

# find_all returns a list of tables
len(tables)

# we want the fourth one (starts at 0, so it's 3)
results_table = tables[3]

# adp_table another nested tag, so call find_all again
rows = results_table.find_all('tr')

# this is a header row
rows[0]

# data rows
first_data_row = rows[1]
first_data_row

rows = results_table.find_all('tr')

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

first_data_row.find_all('td')[2]

first_data_row.find_all('td')[2].find('a').string

def string_from_simple_or_a(td):
    # first try to find the string
    # if it exists, just return that
    simple_string = td.string
    if simple_string is not None:
        return str(simple_string)

    else:
        # if there is no string, try to find a link
        a_tag = td.find('a')

        # if that exists, return that - otherwise return None
        if a_tag is not None:
            return str(a_tag.string)
        else:
            return None


[string_from_simple_or_a(x) for x in first_data_row.find_all('td')]


# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [string_from_simple_or_a(x) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df

# clean up formatting
df.columns = ['standings', 'logo', 'team', 'matches', 'wins', 'draws',
              'losses', 'goals', 'diff', 'points']

df.head()

df = df[[x for x in df.columns if x != 'logo']]
df.head()

df['goals_for'] = df['goals'].str[:2]
df['goals_against'] = df['goals'].str[3:]

df.head()

# column types
int_cols = ['standings', 'matches', 'wins', 'draws', 'losses', 'diff',
            'points', 'goals_for', 'goals_against']

df[int_cols] = df[int_cols].astype(int)

# done
df.head()

