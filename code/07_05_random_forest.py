import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# on goal or not
dfs = dfs.loc[dfs['shot_loc'].notnull()]
dfs['on_goal'] = dfs['shot_loc'].str[0] == 'g'

cont_vars = ['dist', 'time', 'counter', 'x1', 'y1']
cat_vars = ['foot', 'period']

df_cat = pd.concat([pd.get_dummies(dfs[x]) for x in cat_vars], axis=1)
dfs = pd.concat([dfs, df_cat], axis=1)

xvars = cont_vars + list(df_cat.columns)
yvar = 'on_goal'

train, test = train_test_split(dfs, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['on_goal_hat'] = model.predict(test[xvars])
test['correct'] = (test['on_goal_hat'] == test['on_goal'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()
probs.columns = ['pmiss', 'p_on_goal']

results = pd.concat([
    test[['name', 'event_id', 'foot', 'x1', 'y1', 'time', 'on_goal', 'on_goal_hat', 'correct']],
    probs[['p_on_goal']]], axis=1)

results.sample(15)

results['p_on_goal_bin'] = pd.cut(results['p_on_goal'], 10)

results.groupby('p_on_goal_bin')['on_goal'].mean()

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, dfs[xvars], dfs[yvar], cv=10)

scores
scores.mean()

# feature importance
model.fit(dfs[xvars], dfs[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

# vs logit model
dfs['ln_dist'] = np.log(dfs['dist'].apply(lambda x: max(x, 0.5)))
dfs['on_goal'] = dfs['on_goal'].astype(int)
y, X = dmatrices('on_goal ~ dist', dfs)

model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=10)

scores
scores.mean()
