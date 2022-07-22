"""
Answers to the end of chapter exercise for api problems.
"""

import requests
from pandas import DataFrame
import pandas as pd

# given urls
url_adp = 'https://api.myfantasyleague.com/2019/export?TYPE=adp&JSON=1'
url_player = 'https://api.myfantasyleague.com/2019/export?TYPE=players&JSON=1'

# call w/ requests
resp_adp = requests.get(url_adp)
resp_player = requests.get(url_player)

# need to inspect the .json() results in the REPL to see what we want/can turn
# into a DataFrame -- usually list of dicts
df_adp = DataFrame(resp_adp.json()['adp']['player'])
df_player = DataFrame(resp_player.json()['players']['player'])

# now combine
df = pd.merge(df_adp, df_player)

# get rid of IDP players, take top 200
df = df.query("position in ('WR', 'RB', 'TE', 'QB', 'Def', 'PK')")
df = df.head(200)
