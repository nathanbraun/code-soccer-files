import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# load player-game data
pg = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

# book picks up here:

# creating and modifying columns
pg['yellow_cards'] = 1
pg[['name', 'min', 'yellow_cards']].head()

pg['yellow_cards'] = 2
pg[['name', 'min', 'yellow_cards']].head()

# math and number columns
pg['shot_pct'] = 100*pg['goal']/pg['shot']

pg[['name', 'shot', 'goal', 'shot_pct']].head()

import numpy as np  # note: normally you'd import this at the top of the file

pg['biggest_impact'] = np.abs(pg['player_rank'])

pg['ln_pass'] = np.log(pg['pass'])

pg['goal_width_ft'] = 24

pg[['name', 'team', 'match_id', 'goal_width_ft']].sample(5)

# string Columns
pg['name'].str.upper().sample(5)

pg['name'].str.replace('.', ' ').sample(5)

(pg['name'] + ', ' + pg['pos'] + ' - ' + pg['team']).sample(5)

pg['name'].str.replace('.', ' ').str.lower().sample(5)

# boolean columns
pg['is_defender'] = (pg['pos'] == 'DEF')
pg[['name', 'team', 'is_defender']].sample(5)

pg['is_a_mid_or_fwd'] = (pg['pos'] == 'MID') | (pg['pos'] == 'FWD')
pg['balanced_off'] = (pg['goal'] > 0) & (pg['assist'] > 0)
pg['not_fr_or_eng'] = ~((pg['team'] == 'England') | (pg['team'] == 'France'))

(pg[['goal', 'assist']] > 0).sample(5)

# Applying functions to columns
def is_south_america(team):
  """
  Takes some string named team ('England', 'Germany, 'Argentina' etc) and
  checks whether it's in South America.
  """
  return team in ['Brazil', 'Uruguay', 'Colombia', 'Argentina', 'Costa Rica',
                  'Peru']

pg['is_sa'] = pg['team'].apply(is_south_america)

pg[['name', 'team', 'is_sa']].sample(5)

pg['is_sa_alternate'] = pg['team'].apply(lambda x: x in [
    ['Brazil', 'Uruguay', 'Colombia', 'Argentina', 'Costa Rica', 'Peru']])

# Dropping Columns
pg.drop('is_sa_alternate', axis=1, inplace=True)

# Renaming Columns
pg.columns = [x.upper() for x in pg.columns]

pg.head()

pg.columns = [x.lower() for x in pg.columns]

pg.rename(columns={'min': 'minutes'}, inplace=True)

# missing data
pg['shot_pct'] = pg['goal']/pg['shot']
pg[['name', 'team', 'goal', 'shot', 'shot_pct']].head(10)

pg['shot_pct'].isnull().head(10)

pg['shot_pct'].notnull().head(10)

pg['shot_pct'].fillna(-99).head(10)

# Changing column types
pg['date'].sample(5)

date = '20180618'

year = date[0:4]
month = date[4:6]
day = date[6:8]

year
month
day

# pg['month'] = pg['date'].str[4:6]  # commented out since it gives an error

pg['month'] = pg['date'].astype(str).str[4:6]
pg[['name', 'team', 'month', 'date']].sample(5)

pg['month'].astype(int).sample(5)

pg.dtypes.head()
