"""
Answers to the end of chapter exercises for Modeling chapter.
"""
import pandas as pd
import random
from pandas import DataFrame, Series
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

###############################################################################
# problem 7.1
###############################################################################

###################
# from 07_01_ols.py
###################
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

df['dist_m_sq'] = df['dist_m']**2
df['goal'] = df['goal'].astype(int)

model = smf.ols(formula='goal ~ dist_m + dist_m_sq', data=df)
results = model.fit()

def prob_of_goal(meters):
    b0, b1, b2 = results.params
    return (b0 + b1*meters + b2*(meters**2))

df['goal_hat'] = results.predict(df)

#########################
# answers to question 7.1
#########################
# a
df['goal_hat_alt'] = df['dist_m'].apply(prob_of_goal)

df[['goal_hat', 'goal_hat_alt']].head()

# check whether goal_hat and goal_hat_lat are within some epsilon
(df['goal_hat'] == df['goal_hat_alt']).all()

import numpy as np
(np.abs(df['goal_hat'] - df['goal_hat_alt']) < .00000001).all()

# b
model_b = smf.ols(formula='goal ~ dist_m + dist_m_sq + C(period)',
                  data=df)
results_b = model_b.fit()
results_b.summary2()

# c
"""
There just isn't as much shot data from the extra periods (~40 shots total vs
~1300 in periods 1-2). Every game has 2 periods for sure; most games don't have
extra periods. So with a lot less data things can be much more noisy/random and
it's hard to get a clear signal of what's going on.

It'd be like flipping a coin 4 times and trying to make a judgement about
whether it's fair or not.
"""

# d
df['is_2h'] = df['period'] == '2H'
df['is_e1'] = df['period'] == 'E1'
df['is_e2'] = df['period'] == 'E2'

model_d = smf.ols(formula='goal ~ dist_m + dist_m_sq + is_2h + is_e1 + is_e2',
                  data=df)
results_d = model_d.fit()
results_d.summary2()  # yes


###############################################################################
# problem 7.2
###############################################################################

# a
def run_sim_get_pvalue():
    coin = ['H', 'T']

    # make empty DataFrame
    df = DataFrame(index=range(100))

    # now fill it with a "guess"
    df['guess'] = [random.choice(coin) for _ in range(100)]

    # and flip
    df['result'] = [random.choice(coin) for _ in range(100)]

    # did we get it right or not?
    df['right'] = (df['guess'] == df['result']).astype(int)

    model = smf.ols(formula='right ~ C(guess)', data=df)
    results = model.fit()

    return results.pvalues['C(guess)[T.T]']

# b
sims_1k = Series([run_sim_get_pvalue() for _ in range(1000)])
sims_1k.mean()  # 0.5083

# c
def runs_till_threshold(i, p=0.05):
    pvalue = run_sim_get_pvalue()
    if pvalue < p:
        return i
    else:
        return runs_till_threshold(i+1, p)

sim_time_till_sig_100 = Series([runs_till_threshold(1) for _ in range(100)])

# d

# According to Wikipedia, the mean and median of the Geometric distribution are
# 1/p and -1/log_2(1-p). Since we're working with a p of 0.05, that'd give us:

from math import log
p = 0.05
g_mean = 1/p  # 20
g_median = -1/log(1-p, 2)  # 13.51

g_mean, g_median

sim_time_till_sig_100.mean()
sim_time_till_sig_100.median()

###############################################################################
# problem 7.3
###############################################################################

dftm = pd.read_csv(path.join(DATA_DIR, 'team_match.csv'))

# a) Run a logit model regressing three point percentage, offensive and defensive
#    rebounds, steals, turnovers and blocks on whether a team wins.

# a
dftm['win'] = dftm['win'].astype(int)
dftm['npass'] = dftm['pass']

model_a = smf.logit(formula=
                    """
                    win ~ shot + npass
                    """, data=dftm)
results_a = model_a.fit()
results_a.summary2()

margeff = results_a.get_margeff()
margeff.summary()

# b
model_b = smf.logit(formula=
                    """
                    win ~ shot + npass + goal
                    """, data=dftm)
results_b = model_b.fit()
results_b.summary2()

###############################################################################
# problem 7.4
###############################################################################
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

dfpm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

xvars = ['min', 'shot', 'goal', 'goal_allowed', 'assist', 'pass',
    'pass_accurate', 'tackle', 'accel', 'counter', 'opportunity', 'keypass',
    'own_goal', 'interception', 'smart', 'clearance', 'cross', 'air_duel',
    'air_duel_won', 'throw', 'corner', 'started']

yvar = 'pos'

# answer for (c) -- filling missing variables with a negative number in a
# random forest works because the algorithm picks a split point on each
# variable

# so if we have a bunch of normal values for (say) shots, 0, 1, 0, 2
# etc, then we have some that are missing with values -99, the algorithm will
# just pick a split point somewhere between -99 and 0, where everything below
# will go one way, above another
# it works as a way for the CART algorithm to clearly ID/set aside/handle
# missing values

dfpm[xvars] = dfpm[xvars].fillna(-99)

model = RandomForestClassifier(n_estimators=100)

scores = cross_val_score(model, dfpm[xvars], dfpm[yvar], cv=10)

scores.mean()  
scores.min()
scores.max()

# feature important on model
model.fit(dfpm[xvars], dfpm[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

# pass_accurate most important
