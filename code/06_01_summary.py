import pandas as pd
from pandas import DataFrame
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from os import path
import matplotlib.image as mpimg

%matplotlib qt

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'
FIG_DIR = './figures'

###############
# distributions
###############

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfpm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))
dfm = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
dftm = pd.read_csv(path.join(DATA_DIR, 'team_match.csv'))

# processing
dfpm = pd.merge(dfpm, dfm[['match_id', 'home_team', 'away_team']], how='left')
dfpm['opp'] = pd.NA
dfpm.loc[dfpm['team'] == dfpm['home_team'], 'opp'] = dfpm['away_team']
dfpm.loc[dfpm['team'] == dfpm['away_team'], 'opp'] = dfpm['home_team']

dfp = pd.merge(dfp, dft[['team_id', 'grouping']], how='left')

dfs['min_period'] = dfs['time'] // 60

dfs = pd.merge(dfs, dft[['team_id', 'team']], how='left')

###############
# summary stats
###############

# quantile function and describe

dfpm['pass'].quantile(.9)
dfpm[['pass', 'shot']].describe()

dfpm['shot'].value_counts(normalize=True).sort_index().head(10)

##########
# plotting
##########

# basic displot - all on one line
g = (sns.FacetGrid(dfpm).map(sns.kdeplot, 'pass', fill=True))
g.set(xlim=(-5, 120))

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(dfpm)
     .map(sns.kdeplot, 'dist', fill=True))

# hue
g = (sns.FacetGrid(dfpm, hue='pos')
     .map(sns.kdeplot, 'pass', fill=True)
     .add_legend()
     .set(xlim=(-5, 120)))

# add col
g = (sns.FacetGrid(dfpm, hue='pos', col='side')
     .map(sns.kdeplot, 'pass', fill=True)
     .add_legend()
     .set(xlim=(-5, 120)))

# add col order
g = (sns.FacetGrid(dfpm, hue='pos', col='side', col_order=['left', 'central',
                       'right'])
     .map(sns.kdeplot, 'pass', fill=True)
     .add_legend()
     .set(xlim=(-5, 160)))

# rows
dfpm.loc[dfpm['pos'] == 'GKP', 'side'] = 'central'
g = (sns.FacetGrid(dfpm, hue='pos', col='side', row='pos',
                   col_order=['left', 'central', 'right'],
                   row_order=['FWD', 'MID', 'DEF', 'GKP'],
                   )
     .map(sns.kdeplot, 'pass', fill=True)
     .add_legend()
     .set(xlim=(-5, 160)))


#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (goals)
# so we need goals in one column, then another type for scoring type

# book picks up again here:
(dfm[['date', 'home_team', 'away_team', 'home_score', 'away_score']]
 .sort_values('date').head())

def home_away_score_df(df, location):
    df = df[['match_id', 'date', f'{location}_team', f'{location}_score']].copy()
    df.columns = ['match_id', 'date', 'team', 'score']
    df['location'] = location
    return df

home_away_score_df(dfm, 'home').head()

score_long = pd.concat([
    home_away_score_df(dfm, loc) for loc in ['home', 'away']],
    ignore_index=True)

# now can plot points by scoring system and position
g = (sns.FacetGrid(score_long, hue='location')
     .map(sns.kdeplot, 'score', fill=True))
g.add_legend()

#################################
# relationships between variables
#################################

# basic scatter plot
g = sns.relplot(x='weight', y='height', data=dfp)

# with hue
g = sns.relplot(x='weight', y='height', hue='pos', data=dfp)

# adding jitter
import random

random.uniform(0, 1)
[random.gauss(0, 1) for _ in range(10)]

dfp['jheight'] = dfp['height'].apply(lambda x: x + random.gauss(0, 1))
dfp['jweight'] = dfp['weight'].apply(lambda x: x + random.gauss(0, 1))

# col argument
g = sns.relplot(x='jweight', y='jheight', hue='pos', col='team', col_wrap=5,
                data=dfp)

# distribution of weight by team
# note -- for plot in book did some minor labeling/reordering using hue_order
# and label_order arguments
g = (sns.FacetGrid(dfp, hue='team', col='grouping', col_wrap=2, aspect=2,
                   col_order=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    .map(sns.kdeplot, 'weight', fill=True)
    .add_legend())

# contour plots
# fill
g = (sns.FacetGrid(dfp, col='pos', hue='pos', col_wrap=2, aspect=2)
     .map(sns.kdeplot, 'weight', 'height', fill=True))

# no fill
g = (sns.FacetGrid(dfp, col='pos', hue='pos', col_wrap=2, aspect=2)
     .map(sns.kdeplot, 'weight', 'height'))

##############
# correlations
##############
dftm[['shot', 'goal', 'shot_opp', 'goal_opp', 'pass_opp', 'pass', 'win']].corr().round(2)

sns.relplot(x='shot', y='goal', data=dftm)

dftm['jshot'] = dftm['shot'].apply(lambda x: x + random.gauss(0, 1))
dftm['jgoal'] = dftm['goal'].apply(lambda x: x + random.gauss(0, 1))

sns.relplot(x='jshot', y='jgoal', data=dftm)

sns.relplot(x='jshot', y='pass', data=dftm)

# passes vs player rank
sns.relplot(x='pass', y='player_rank', data=dfpm)
plt.show()

# passes vs player rank - by position
sns.relplot(x='pass', y='player_rank', hue='pos', data=dfpm)
plt.show()

# passes vs player rank - by position and team
sns.relplot(x='pass', y='player_rank', hue='pos', col='team', data=dfpm,
            col_wrap=4)

########################
# line plots with python
########################

dfm['total_goals'] = dfm['home_score'] + dfm['away_score']

# note: day is overall day of the tournament
g = sns.relplot(x='day', y='total_goals', kind='line', data=dfm)

ave_total_goals = dfm.groupby('day')['total_goals'].mean().reset_index()
g = sns.relplot(x='day', y='total_goals', kind='line', data=ave_total_goals)

# shot distance by foot/minute
g = sns.relplot(x='min_period', y='dist_m', kind='line', hue='foot',
                data=dfs.query("period in ('1H', '2H')"),
                row='period')

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(dfpm, col='pos')
     .map(sns.kdeplot, 'pass', fill=True))

# wrap columns
g = (sns.FacetGrid(dfpm, col='pos', col_wrap=2)
     .map(sns.kdeplot, 'pass', fill=True))

# adding a title
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('Distribution of No of Passes by Position')

# modifying options
g.set(xlim=(-5, 120))

g.set_xlabels('Passes')
g.set_ylabels('Density')

# saving
g.savefig(path.join(FIG_DIR, 'no_passes_by_position.png'))
