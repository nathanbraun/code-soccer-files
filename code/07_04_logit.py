import pandas as pd
import math
import statsmodels.formula.api as smf
from os import path

DATA_DIR = '/Users/nathan/fantasybook/data'

#####################
# logistic regression
#####################

# load
df = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))

# process
df = df.loc[(df['play_type'] == 'run') | (df['play_type'] == 'pass')]
df['offensive_td'] = ((df['touchdown'] == 1) & (df['yards_gained'] > 0))
df['offensive_td'] = df['offensive_td'].astype(int)
df['yardline_100_sq'] = df['yardline_100'] ** 2

# run regression
model = smf.logit(formula='offensive_td ~ yardline_100 + yardline_100_sq',
                  data=df)
results = model.fit()
results.summary2()

def prob_of_td(yds):
    b0, b1, b2 = results.params
    value = (b0 + b1*yds + b2*(yds**2))
    return 1/(1 + math.exp(-value))

prob_of_td(75)
prob_of_td(25)
prob_of_td(5)
