import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = './data'

df = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

xvars = ['shot', 'goal', 'assist', 'pass', 'pass_accurate', 'tackle', 'accel',
        'counter', 'opportunity', 'keypass', 'own_goal', 'interception',
        'smart', 'clearance', 'cross', 'air_duel', 'air_duel_won',
        'gk_leave_line', 'gk_save_attempt', 'throw', 'corner', 'started']

yvar = 'pos'

df[xvars + [yvar]].head()
df[yvar].value_counts(normalize=True)

train, test = train_test_split(df, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['pos_hat'] = model.predict(test[xvars])
test['correct'] = (test['pos_hat'] == test[yvar])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)

probs.head()

results = pd.concat([
    test[['name', 'team', 'pos', 'pos_hat', 'correct']],
    probs], axis=1)

results.sample(10).round(2)

results.groupby('pos')[['correct', 'FWD', 'MID', 'DEF', 'GKP']].mean()

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, df[xvars], df[yvar], cv=10)

scores
scores.mean()

# feature importance
model = RandomForestClassifier(n_estimators=100)
model.fit(df[xvars], df[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)
