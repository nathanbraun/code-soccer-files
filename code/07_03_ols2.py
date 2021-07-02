import pandas as pd
import numpy as np
import math
import statsmodels.formula.api as smf
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))

dfs['goal'] = dfs['goal'].astype(int)
dfs['header'] = dfs['foot'] == 'head/body'

#########################
# holding things constant
#########################

# header
model = smf.ols(formula=
        """
        goal ~ header
        """, data=dfs)
results = model.fit()
results.summary2()

# fine but headers are close
model = smf.ols(formula=
        """
        goal ~ header + dist
        """, data=dfs)
results = model.fit()
results.summary2()

###############
# fixed effects
###############

# shot location
shot_on_goal = dfs['shot_loc_desc'].str.startswith('goal').fillna(False)
dfs['on_goal_loc'] = dfs['shot_loc_desc'].str.replace('goal ', '')

model = smf.ols(formula="goal ~ C(on_goal_loc) + dist", data=dfs.loc[shot_on_goal])
results = model.fit()
results.summary2()

####################
# squaring variables
####################

dfs['dist2'] = dfs['dist'] ** 2
model = smf.ols(formula="goal ~ dist + dist2", data=dfs)
results = model.fit()
results.summary2()

# cubed variables
dfs['dist3'] = dfs['dist'] ** 3
model = smf.ols(formula="goal ~ dist + dist2 + dist3", data=dfs)
results = model.fit()
results.summary2()

#############
# natural log
#############
dfs['ln_dist'] = np.log(dfs['dist'])

model = smf.ols(formula='goal ~ ln_dist', data=dfs)
results = model.fit()
results.summary2()

#############
# intractions
#############

dfp['player_dom_foot'] = dfp['foot']
dfs = pd.merge(dfs, dfp[['player_id', 'pos', 'player_dom_foot']])

dfs['dominant'] = np.nan
dfs.loc[dfs['foot'] == dfs['player_dom_foot'], 'dominant'] = 'dominant'
dfs.loc[dfs['foot'] != dfs['player_dom_foot'], 'dominant'] = 'non dominant'
dfs.loc[dfs['foot'] == 'head/body', 'dominant'] = 'head/body'

# dominant
model = smf.ols(formula=
        """
        goal ~ ln_dist*C(dominant)
        """, data=dfs)
results = model.fit()
results.summary2()

#######
# logit
#######
dfs['header'] = dfs['foot'] == 'head/body'

model = smf.logit(formula=
        """
        goal ~ header + ln_dist
        """, data=dfs)
logit_results = model.fit()
logit_results.summary2()

def prob_goal(dist, is_header):
    b0, b1, b2 = logit_results.params
    value = (b0 + b1*is_header + b2*np.log(dist))
    return 1/(1 + math.exp(-value))

prob_goal(20, 0)
prob_goal(14, 1)
prob_goal(14, 0)
