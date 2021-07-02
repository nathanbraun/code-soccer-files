import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

shots = pd.read_csv(path.join(SO, 'shots.csv'))  # shot data

# Granularity

# Grouping
# TODO: make shot distance from this
shots.groupby('match_id').sum()

shots['attempt'] = 1

sum_cols = ['goal', 'attempt', 'accurate', 'counter', 'opportunity']
shots.groupby('match_id').sum()[sum_cols]

shots.groupby('match_id').agg({
    'goal': 'sum',
    'attempt': 'count',
    'dist': ['mean', 'min', 'max']})

shots.groupby('match_id').agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist = ('dist', 'mean'),
    min_dist = ('dist', 'min'),
    max_dist = ('dist', 'max'))

shots_team = shots.groupby(['match_id', 'team_id']).agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist = ('dist', 'mean'),
    min_dist = ('dist', 'min'),
    max_dist = ('dist', 'max'))

shots_team.head()

# A note on multilevel indexing
shots_team.loc[[(2057954, 14358), (2058017, 4418)]]

# Stacking and unstacking data
fd = shots.query("foot in ('left', 'right')").groupby(['name', 'foot'])['dist'].mean().reset_index()

fd_reshaped = fd.set_index(['name', 'foot']).unstack()
fd_reshaped.head()

fd_reshaped.columns = ['left', 'right']

fd_reshaped.idxmax(axis=1).value_counts()

fd_reshaped_undo = fd_reshaped.stack()
fd_reshaped_undo.head()
