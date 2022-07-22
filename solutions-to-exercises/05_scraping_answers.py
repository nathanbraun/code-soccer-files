"""
Answers to the end of chapter exercises for scraping problems.
"""

from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

ffc_base_url = 'https://fantasyfootballcalculator.com'

###############################################################################
# 5.1.1
###############################################################################
def scrape_ffc(scoring, nteams, year):
    # build URL based on arguments
    ffc_url = (ffc_base_url + '/adp' + _scoring_helper(scoring) +
               f'/{nteams}-team/all/{year}')
    ffc_response = requests.get(ffc_url)

    # all same as 05_01_scraping.py file
    adp_soup = Soup(ffc_response.text)
    tables = adp_soup.find_all('table')
    adp_table = tables[0]
    rows = adp_table.find_all('tr')

    # move parse_row to own helper function
    list_of_parsed_rows = [_parse_row(row) for row in rows[1:]]

    # put it in a dataframe
    df = DataFrame(list_of_parsed_rows)

    # clean up formatting
    df.columns = ['ovr', 'pick', 'name', 'pos', 'team', 'adp', 'std_dev',
                'high', 'low', 'drafted', 'graph']

    float_cols =['adp', 'std_dev']
    int_cols =['ovr', 'drafted']

    df[float_cols] = df[float_cols].astype(float)
    df[int_cols] = df[int_cols].astype(int)

    df.drop('graph', axis=1, inplace=True)

    return df

# helper functions - just moving some logic to own section
def _scoring_helper(scoring):
    """
    Take a scoring system (either 'ppr', 'half', 'std') and return the correct
    FFC URL fragment.

    Note: helper functions are often prefixed with _, but it's not required.
    """
    if scoring == 'ppr':
        return '/ppr'
    elif scoring == 'half':
        return '/half-ppr'
    elif scoring == 'std':
        return '/standard'

def _parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

###############################################################################
# 5.1.2
###############################################################################
def scrape_ffc_plus(scoring, nteams, year):
    # build URL based on arguments
    ffc_url = ffc_base_url + '/adp' + _scoring_helper(scoring) + f'/{nteams}-team/all/{year}'
    ffc_response = requests.get(ffc_url)

    # all same as 05_01_scraping.py file
    adp_soup = Soup(ffc_response.text)
    tables = adp_soup.find_all('table')
    adp_table = tables[0]
    rows = adp_table.find_all('tr')

    # move parse_row to own helper function
    list_of_parsed_rows = [_parse_row_with_link(row) for row in rows[1:]]

    # put it in a dataframe
    df = DataFrame(list_of_parsed_rows)

    # clean up formatting
    df.columns = ['ovr', 'pick', 'name', 'pos', 'team', 'adp', 'std_dev',
                  'high', 'low', 'drafted', 'graph', 'link']

    float_cols =['adp', 'std_dev']
    int_cols =['ovr', 'drafted']

    df[float_cols] = df[float_cols].astype(float)
    df[int_cols] = df[int_cols].astype(int)

    df.drop('graph', axis=1, inplace=True)

    return df

def _parse_row_with_link(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings, also get link.
    """
    # parse the row like before and save it into a list
    parsed_row = [str(x.string) for x in row.find_all('td')]

    # now get the link, which is the href attribute of the first 'a' tag
    link = ffc_base_url + str(row.find_all('a')[0].get('href'))

    # add link onto the end of the list and return
    return parsed_row + [link]

###############################################################################
# 5.1.3
###############################################################################
def ffc_player_info(url):
    ffc_response = requests.get(url)
    player_soup = Soup(ffc_response.text)

    # info is in multiple tables, but can get all rows with shortcut
    rows = player_soup.find_all('tr')

    list_of_parsed_rows = [_parse_row(row) for row in rows]

    # this is a list of two item lists [[key1, value1], [key2, value2], ...],
    # so we're unpacking each key, value pair with for key, value in ...
    dict_of_parsed_rows = {key: value for key, value in list_of_parsed_rows}

    # now modify slightly to return what we want, which (per problem
    # instructions) is team, height, weight, birthday, and draft info
    return_dict = {}
    return_dict['team'] = dict_of_parsed_rows['Team:']
    return_dict['height'] = dict_of_parsed_rows['Ht / Wt:'].split('/')[0]
    return_dict['weight'] = dict_of_parsed_rows['Ht / Wt:'].split('/')[1]
    return_dict['birthday'] = dict_of_parsed_rows['Born:']
    return_dict['drafted'] = dict_of_parsed_rows['Drafted:']
    return_dict['draft_team'] = dict_of_parsed_rows['Draft Team:']

    return return_dict

# note: we haven't talked about if __name__ == '__main__'
# it' Python convention to put all your useful functions above this part, and
# the code that actually calls it below
# this way the test code doesn't get run if you import scrape_ffc to use in
# another file
# don't worry too much about this
if __name__ == '__main__':
    # testing 5.1.1
    ppr_12_2016 = scrape_ffc('ppr', 12, 2016)
    std_12_2011 = scrape_ffc('std', 12, 2011)
    half_12_2018 = scrape_ffc('std', 12, 2018)

    # testing 5.1.2
    ppr_12_2015 = scrape_ffc_plus('ppr', 12, 2015)
    std_12_2012 = scrape_ffc_plus('std', 12, 2012)
    half_12_2019 = scrape_ffc_plus('std', 12, 2019)

    # testing 5.1.3
    # 'https://fantasyfootballcalculator.com/adp/players/adrian-peterson'
    test_link = ppr_12_2015['link'].iloc[0]
    ffc_player_info(test_link)
