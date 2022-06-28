import pandas as pd
import numpy as np
import math
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))

dfs['goal'] = dfs['goal'].astype(int)
dfs['header'] = dfs['foot'] == 'head/body'
dfs['dist_sq'] = dfs['dist'] ** 2

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

dfs.groupby('header')['dist'].mean()

# fine but headers are close
model = smf.ols(formula=
        """
        goal ~ header + dist
        """, data=dfs)
results = model.fit()
results.summary2()

0.2769 - 0.0086*20
0.2769 - 0.0086*9 - 0.0345

###############
# fixed effects
###############

pd.get_dummies(dfs['foot']).head()

model = smf.ols(formula="goal ~ C(foot) + dist + dist_sq", data=dfs)
results = model.fit()
results.summary2()

dfs['foot'].value_counts()

model = smf.ols(formula="goal ~ C(foot, Treatment(reference='right')) + dist + dist_sq", data=dfs)
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

dfs['is_header'] = dfs['foot'] == 'head/body'

model = smf.ols(formula=
        """
        goal ~ dist + dist:is_header
        """, data=dfs)
results = model.fit()
results.summary2()

#######
# logit
#######
model = smf.logit(formula=
        """
        goal ~ dist + dist:is_header
        """, data=dfs)
logit_results = model.fit()
logit_results.summary2()

def prob_goal_logit(dist, is_header):
    b0, b1, b2  = logit_results.params
    value = (b0 + b1*dist + b2*dist*is_header) 
    return 1/(1 + math.exp(-value))

prob_goal_logit(20, 0)
prob_goal_logit(14, 1)
prob_goal_logit(14, 0)
