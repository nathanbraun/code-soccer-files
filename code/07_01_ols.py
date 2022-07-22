import pandas as pd
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

###################
# linear regression
###################

# load
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

df['dist_m_sq'] = df['dist_m']**2
df['goal'] = df['goal'].astype(int)

df[['goal', 'dist_m', 'dist_m_sq']].head()

model = smf.ols(formula='goal ~ dist_m + dist_m_sq', data=df)
results = model.fit()

results.summary2()

def prob_of_goal(meters):
    b0, b1, b2 = results.params
    return (b0 + b1*meters + b2*(meters**2))

prob_of_goal(1)
prob_of_goal(15)
prob_of_goal(25)

# process
df['goal_hat'] = results.predict(df)
df[['goal', 'goal_hat']].head(5)

model = smf.ols(formula='goal ~ dist_m + dist_m_sq + C(period)', data=df)
results = model.fit()
results.summary2()
