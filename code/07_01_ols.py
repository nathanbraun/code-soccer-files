import pandas as pd
import statsmodels.formula.api as smf
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'

###################
# linear regression
###################

# load
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

df['dist_sq'] = df['dist']**2
df['goal'] = df['goal'].astype(int)

df[['goal', 'dist', 'dist_sq']].head()

model = smf.ols(formula='goal ~ dist + dist_sq', data=df)
results = model.fit()

results.summary2()

def prob_of_goal(yds):
    b0, b1, b2 = results.params
    return (b0 + b1*yds + b2*(yds**2))

prob_of_goal(1)
prob_of_goal(25)
prob_of_goal(30)

# process
df['goal_hat'] = results.predict(df)
df[['goal', 'goal_hat']].head(10)

