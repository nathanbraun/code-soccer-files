import requests
from pandas import DataFrame
import pandas as pd

fc_url = 'https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year=2020'

resp = requests.get(fc_url)

df = DataFrame(resp.json()['players'])
df.head()

def fc_adp(scoring='ppr', teams=12, year=2020):
    ffc_com = 'https://fantasyfootballcalculator.com'
    resp = requests.get(
        f'{ffc_com}/api/v1/adp/{scoring}?teams={teams}&year={year}'
    )
    df = DataFrame(resp.json()['players'])

    # data doesn't come with teams, year columns, let's add them
    df['year'] = year
    df['teams'] = teams
    return df

df_10_std = fc_adp('standard', 10, 2019)
df_10_std.head()

df_history = pd.concat(
    [fc_adp('standard', 12, year=y) for y in range(2009, 2020)],
    ignore_index=True)
