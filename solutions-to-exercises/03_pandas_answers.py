"""
Answers to the end of chapter exercises for Pandas chapter.

Questions with written (not code) answers are inside triple quotes.
"""
###############################################################################
# PANDAS BASICS
###############################################################################

#######
# 3.0.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
dfm = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))

#######
# 3.0.2
#######
dfm10 = dfm.sort_values('date').head(10)

#######
# 3.0.3
#######
dfm.sort_values('label', ascending=False, inplace=True)
dfm.head()

# Note: if this didn't work when you printed it on a new line in the REPL you
# probably forgot the `inplace=True` argument.

#######
# 3.0.4
#######
type(dfm.sort_values('label'))  # it's a DataFrame

#######
# 3.0.5
#######
# a
match_simple = dfm[['date', 'home_team', 'away_team', 'home_score',
    'away_score']]

# b
match_simple = match_simple[['home_team', 'away_team', 'date', 'home_score',
    'away_score']]

# c
match_simple['match_id'] = dfm['match_id']

# d
dfm.to_csv(path.join(DATA_DIR, 'match_simple.txt'), sep='|')

###############################################################################
# COLUMNS
###############################################################################

#######
# 3.1.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

#######
# 3.1.2
#######
pm['ob_touches'] = pm['throw'] + pm['corner']
pm['ob_touches'].head()

#######
# 3.1.3
#######
pm['player_desc'] = pm['name'] + ' is the ' + pm['team'] + ' ' + pm['pos']
pm['player_desc'].head()

#######
# 3.1.4
#######
pm['at_least_one_throwin'] = pm['throw'] > 0
pm['at_least_one_throwin'].head()

#######
# 3.1.5
#######
pm['len_last_name'] = (pm['name']
                       .apply(lambda x: len(x.split(' ')[-1])))
pm['len_last_name'].head()

#######
# 3.1.6
#######
pm['match_id'] = pm['match_id'].astype(str)

#######
# 3.1.7
#######
# a
pm.columns = [x.replace('_', ' ') for x in pm.columns]
pm.head()

# b
pm.columns = [x.replace(' ', '_') for x in pm.columns]
pm.head()

#######
# 3.1.8
#######
# a
pm['air_duel_won_percentage'] = pm['air_duel_won']/pm['air_duel']
pm['air_duel_won_percentage'].head()

# b
"""
`'air_duel_won_percentage'` is air duels won divided by total air duels. Since
you can't divide by 0, `air_duel_won_percentage` is missing whenever a player
had 0 rebounds.
"""

# To replace all the missing values with `-99`:
pm['air_duel_won_percentage'].fillna(-99, inplace=True)
pm['air_duel_won_percentage'].head()

#######
# 3.1.9
#######
pm.drop('air_duel_won_percentage', axis=1, inplace=True)
pm.head()

# If you forget the `axis=1` Pandas will try to drop the *row* with the
# index value `'air_duel_won_percentage'`. Since that doesn't exist, it'll throw an
# error.

# Without the `inplace=True`, Pandas just returns a new copy of `pm` without the
# `'air_duel_won_percentage'` column. Nothing happens to the original `pm`, though we
# could reassign it if we wanted like this:

# alternative to inplace=True
# pm = pm.drop('air_duel_won_percentage', axis=1)

###############################################################################
# BUILT-IN FUNCTIONS
###############################################################################
#######
# 3.2.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

#######
# 3.2.2
#######
pm['named_pass1'] = pm['clearance'] + pm['cross'] + pm['assist'] + pm['keypass']

pm['named_pass2'] = pm[['clearance', 'cross', 'assist', 'keypass']].sum(axis=1)

(pm['named_pass1'] == pm['named_pass2']).all()

#######
# 3.2.3
#######

# a
pm[['shot', 'assist', 'pass']].mean()

# shot       0.817475
# assist     0.050269
# pass      31.599641

# b
((pm['goal'] >= 1) & (pm['assist'] >= 1)).sum()  # 10

# c
((pm['goal'] >= 1) & (pm['assist'] >= 1)).sum()/(pm.shape[0])  # 0.5984%

# d
pm['own_goal'].sum()  # 10

# e
pm['pos'].value_counts()  # MID - 636

###############################################################################
# FILTERING
###############################################################################
#######
# 3.3.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))

#######
# 3.3.2
#######
# a
dfp_bra1 = dfp.loc[dfp['team'] == 'Brazil', ['player_name', 'pos', 'foot',
    'weight', 'height']]

dfp_bra1.head()

# b
dfp_bra2 = dfp.query("team == 'Brazil'")[['player_name', 'pos', 'foot',
    'weight', 'height']]
dfp_bra2.head()

#######
# 3.3.3
#######
dfp_no_bra = dfp.loc[dfp['team'] != 'Brazil', ['team', 'player_name', 'pos',
    'foot', 'weight', 'height']]
dfp_no_bra.head()

#######
# 3.3.4
#######

# a
dfp['bday'] = dfp['birth_date'].astype(str).str[-4:]
dfp['bday'].duplicated().any()  # yes there are

# b
# flags ALL dups (not just 2nd) because passing keep=False
dups = dfp[['bday']].duplicated(keep=False)

dfp_dups = dfp.loc[dups]
dfp_no_dups = dfp.loc[~dups]

#######
# 3.3.5
#######
import numpy as np

dfp['height_description'] = np.nan
dfp.loc[dfp['height'] > 190, 'height_description'] = 'tall'
dfp.loc[dfp['height'] < 170, 'height_description'] = 'short'
dfp[['height', 'height_description']].sample(5)

#######
# 3.3.6
#######
# a
dfp_no_desc1 = dfp.loc[dfp['height_description'].isnull()]

# b
dfp_no_desc2 = dfp.query("height_description.isnull()")

###############################################################################
# GRANULARITY
###############################################################################
#######
# 3.4.1
#######
"""
Usually you can only shift your data from more (play by play) to less (game)
granular, which necessarily results in a loss of information. If I go from
knowing which shots Messi scored on (and how much time was left in the match,
etc) to just knowing he scored, say, 2 goals total, that's a loss of
information.
"""

#######
# 3.4.2
#######

# a
import pandas as pd
from os import path

DATA_DIR = './data'
dfpm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

# b
dfpm.groupby('player_id')['shot', 'goal'].mean()

# c
player_ave = dfpm.groupby('player_id')['shot', 'goal'].mean()
(player_ave['shot'] >= 4).mean()  # 1.05%

#######
# 3.4.3
#######

# a
dftm = dfpm.groupby(['match_id', 'team']).agg(
    total_goal = ('goal', 'sum'),
    total_pass = ('pass', 'sum'),
    total_shot = ('shot', 'sum'),
    nplayed = ('player_id', 'count'))

dftm.head()

# b
dftm.reset_index(inplace=True)

# c
dftm['no_goals'] = dftm['total_goal'] == 0
dftm.groupby('no_goals')['total_pass', 'total_shot'].mean()

# d
dftm.groupby('team')['match_id'].count()
dfpm.groupby('team')['match_id'].sum()

"""
Count counts the number of non missing (non `np.nan`) values. This is different
than `sum` which adds up the values in all of the columns. The only time
`count` and `sum` would return the same thing is if you had a column filled
with 1s without any missing values.
"""

#######
# 3.4.4
#######
"""
Stacking is when you change the granularity in your data, but shift information
from rows to columns (or vis versa) so it doesn't result in any loss on
information.
"""

###############################################################################
# COMBINING DATAFRAMES
###############################################################################
#######
# 3.5.1
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
df_name = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'name.csv'))
df_shot = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'shot.csv'))
df_pass = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'pass.csv'))
df_ob = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'ob.csv'))

# b
df_comb1 = pd.merge(df_name, df_shot, how='left')
df_comb1 = pd.merge(df_comb1, df_pass, how='left')
df_comb1 = pd.merge(df_comb1, df_ob, how='left')

df_comb1 = df_comb1.fillna(0)

# c
df_comb2 = pd.concat([df_name.set_index(['player_id', 'match_id']),
                      df_shot.set_index(['player_id', 'match_id']),
                      df_pass.set_index(['player_id', 'match_id']),
                      df_ob.set_index(['player_id', 'match_id'])], join='outer',
                     axis=1)

df_comb2 = df_comb2.fillna(0)

# d
"""
Which is better is somewhat subjective, but I generally prefer `concat` when
combining three or more DataFrames because you can do it all in one step.

Note `merge` gives a little more fine grained control over how you merge (left,
or outer) vs `concat`, which just gives you inner vs outer.

Note also we have to set the index equal to game and player id before
concating.
"""

########
# 3.5.2a
########
import pandas as pd
from os import path

DATA_DIR = './data'
df_d = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'def.csv'))
df_f = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'fwd.csv'))
df_m = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'mid.csv'))

# b
df = pd.concat([df_d, df_f, df_m], ignore_index=True)

#######
# 3.5.3
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# b
for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
    (dft
        .query(f"grouping == '{group}'")
        .to_csv(path.join(DATA_DIR, f'dft_{group}.csv'), index=False))

# c
df = pd.concat([pd.read_csv(path.join(DATA_DIR, f'dft_{group}.csv'))
    for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], ignore_index=True)

