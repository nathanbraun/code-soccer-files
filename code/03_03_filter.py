import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# note: we're passing the index_col argument, which immediately setting the
# index to be the player_id column
dfm = pd.read_csv(path.join(DATA_DIR, 'matches.csv'), index_col='match_id')

# Filtering

championship_id = 2058017
dfm.loc[championship_id]

group_a_ids = [2057959, 2057958, 2057957, 2057956, 2057955, 2057954]

dfm.loc[group_a_ids]
dfm.loc[group_a_ids, ['label', 'group', 'venue']]
dfm.loc[group_a_ids, 'venue']

# Boolean Indexing
is_group_b = dfm['group'] == 'Group B'

is_group_b.head()

dfm_b = dfm.loc[is_group_b]

dfm_b[['label', 'group', 'venue']].head()

dfm_g = dfm.loc[dfm['group'] == 'Group G']
dfm_g[['label', 'group', 'venue']].head()

is_group_d = dfm['group'] == 'Group D'

dfm_not_d = dfm.loc[~is_group_d]

dfm_not_d[['label', 'group', 'venue']].head()

# Duplicates
dfm.drop_duplicates(inplace=True)

dfm.drop_duplicates('venue')[['label', 'group', 'venue']]

dfm.duplicated().head()

dfm['group'].duplicated().head()

# Combining filtering with changing columns

dfm['home_away_desc'] = np.nan
dfm.loc[dfm['home'] == dfm['winner'], 'home_away_desc'] = 'home team won!'
dfm.loc[dfm['away'] == dfm['winner'], 'home_away_desc'] = 'away team won!'
dfm.loc[dfm['winner'] == 0, 'home_away_desc'] = 'tied!'

dfm['home_away_desc'].value_counts()

# Query
dfm.query("group == 'Group A'").head()

dfm['is_group_b'] = dfm['group'] == 'Group B'

dfm.query("is_group_b").head()

dfm.query("group.isnull()")[['label', 'group', 'venue']].head()

# note: if getting an error on line above, try it with engine='python' like
# this
dfm.query("group.isnull()", engine='python')[['label', 'group', 'venue']].head()
