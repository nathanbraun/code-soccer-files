import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

shots = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))  # shot data

# Granularity

# Grouping
# TODO: make shot distance from this
shots.groupby('match_id').sum().head()

shots['attempt'] = 1
sum_cols = ['goal', 'attempt', 'accurate', 'counter', 'opportunity']
shots.groupby('match_id').sum()[sum_cols].head()

shots.groupby('match_id').agg({
    'goal': 'sum',
    'attempt': 'count',
    'dist_m': 'mean',
    'dist_ft': 'mean'}).head()

shots.groupby('match_id').agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist_m = ('dist_m', 'mean'),
    ave_dist_ft = ('dist_ft', 'mean')).head()

shots_team = shots.groupby(['match_id', 'team_id']).agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist_m = ('dist_m', 'mean'),
    min_dist_m = ('dist_m', 'min'),
    max_dist_ft = ('dist_ft', 'max'))

shots_team.head()

# A note on multilevel indexing
shots_team.loc[[(2057954, 14358), (2058017, 4418)]]

# Stacking and unstacking data
fd = shots.query("foot in ('left', 'right')").groupby(
    ['name', 'foot'])['dist_m'].mean().reset_index()
fd.head()

fd_reshaped = fd.set_index(['name', 'foot']).unstack()
fd_reshaped.head()

fd_reshaped.columns = ['left', 'right']
(fd_reshaped['right'] - fd_reshaped['left']).mean()

fd_reshaped.idxmax(axis=1).value_counts()

fd_reshaped_undo = fd_reshaped.stack()
fd_reshaped_undo.head()
