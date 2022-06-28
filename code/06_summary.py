import pandas as pd
from pandas import DataFrame
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from os import path
import matplotlib.image as mpimg

pd.options.mode.chained_assignment = None
%matplotlib qt

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'
FIG_DIR = './figures'

###############
# distributions
###############

pm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

###############
# summary stats
###############

# quantile function and describe

pm['pass'].quantile(.9)
pm[['pass', 'shot']].describe()

##########
# plotting
##########

# basic displot - all on one line
g = (sns.FacetGrid(pm).map(sns.kdeplot, 'pass', shade=True))
g.set(xlim=(-5, 120))
plt.show()

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(pm)
     .map(sns.kdeplot, 'dist', shade=True))

# hue
g = (sns.FacetGrid(pm, hue='pos')
     .map(sns.kdeplot, 'pass', shade=True)
     .add_legend()
     .set(xlim=(-5, 120)))
plt.show()

# add col
g = (sns.FacetGrid(pm, hue='pos', col='side')
     .map(sns.kdeplot, 'pass', shade=True)
     .add_legend()
     .set(xlim=(-5, 120)))
plt.show()

# add col order
g = (sns.FacetGrid(pm, hue='pos', col='side', col_order=['left', 'central',
                       'right'])
     .map(sns.kdeplot, 'pass', shade=True)
     .add_legend()
     .set(xlim=(-5, 160)))
plt.show()

# rows
pm.loc[pm['pos'] == 'GKP', 'side'] = 'central'
g = (sns.FacetGrid(pm, hue='pos', col='side', row='pos',
                   col_order=['left', 'central', 'right'],
                   row_order=['FWD', 'MID', 'DEF', 'GKP'],
                   )
     .map(sns.kdeplot, 'pass', shade=True)
     .add_legend()
     .set(xlim=(-5, 160)))


#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (goals)
# so we need goals in one column, then another type for scoring type

matches = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))

# book picks up again here:
matches[['home_team', 'away_team', 'home_score', 'away_score']].head()  # have this

def home_away_score_df(_df, location):
    _df = _df[['match_id', 'date', f'{location}_team', f'{location}_score']]
    _df.columns = ['match_id', 'date', 'team', 'score']
    _df['location'] = location
    return _df

home_away_score_df(matches, 'home').head()

score_long = pd.concat([
    home_away_score_df(matches, loc) for loc in ['home', 'away']],
    ignore_index=True)

# now can plot points by scoring system and position
g = (sns.FacetGrid(score_long, hue='location')
     .map(sns.kdeplot, 'score', shade=True))
g.add_legend()
plt.show()

#################################
# relationships between variables
#################################

dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))

# basic scatter plot
g = sns.relplot(x='weight', y='height', data=dfp)

# with hue
g = sns.relplot(x='jweight', y='jheight', hue='pos', data=dfp)

# adding jitter
import random

random.uniform(0, 1)
[random.gauss(0, 1) for _ in range(10)]

dfp['jheight'] = dfp['height'].apply(lambda x: x + random.gauss(0, 1))
dfp['jweight'] = dfp['weight'].apply(lambda x: x + random.gauss(0, 1))

# col argument
g = sns.relplot(x='jweight', y='jheight', hue='pos', col='team', col_wrap=5,
                data=dfp)

# scatter plot
g = (sns.FacetGrid(dfp, hue='team')
    .map(sns.kdeplot, 'weight', shade=True)
    .add_legend())

# load match data
matches = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))
pm = pd.merge(pm, matches[['match_id', 'home_team', 'away_team']], how='left')
pm['opp'] = np.nan
pm.loc[pm['team'] == pm['home_team'], 'opp'] = pm['away_team']
pm.loc[pm['team'] == pm['away_team'], 'opp'] = pm['home_team']

# group player data to team level
_tm = pm.groupby(['team', 'opp', 'match_id'])[['shot', 'goal', 'assist', 'pass',
    'pass_accurate', 'tackle', 'accel', 'counter', 'opportunity', 'keypass',
    'own_goal', 'interception', 'smart', 'clearance', 'cross', 'air_duel',
    'air_duel_won', 'gk_leave_line', 'gk_save_attempt', 'throw',
    'corner']].sum().reset_index()

tm = pd.merge(_tm, _tm.drop('opp', axis=1), left_on=['match_id', 'opp'],
               right_on=['match_id', 'team'], suffixes=('', '_opp'))
tm['win'] = tm['goal'] > tm['goal_opp']

# book picks back up here
# correlations
tm[['shot', 'goal', 'shot_opp', 'goal_opp', 'pass_opp', 'pass', 'win']].corr().round(2)

sns.relplot(x='shot', y='goal', data=tm)

tm['jshot'] = tm['shot'].apply(lambda x: x + random.gauss(0, 1))
tm['jgoal'] = tm['goal'].apply(lambda x: x + random.gauss(0, 1))

sns.relplot(x='jshot', y='jgoal', data=tm)

sns.relplot(x='jshot', y='pass', data=tm)

# passes vs player rank
sns.relplot(x='pass', y='player_rank', data=pm)
plt.show()

# passes vs player rank - by position
sns.relplot(x='pass', y='player_rank', hue='pos', data=pm)
plt.show()

# passes vs player rank - by position and team
sns.relplot(x='pass', y='player_rank', hue='pos', col='team', data=pm,
            col_wrap=4)

########################
# line plots with python
########################

# let's look at scoring by week

# minor processing

matches['day'] = (pd.to_datetime(matches['date']) -
    pd.to_datetime(matches['date'].min())).dt.days
matches['total_goals'] = matches['home_score'] + matches['away_score']

g = sns.relplot(x='day', y='total_goals', kind='line', data=matches)

ave_total_goals = matches.groupby('day')['total_goals'].sum().reset_index()
g = sns.relplot(x='day', y='total_goals', kind='line', data=ave_total_goals)

# by group
g = sns.relplot(x='day', y='score', kind='line', data=score_long,
                hue='group', col='group', col_wrap=4)

# by team (just the line)
g = sns.relplot(x='day', y='score', kind='line', data=score_long,
                hue='team', col='group', col_wrap=4)

# shot distance by foot/minute
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

dfs['min_period'] = dfs['time'] // 60
g = sns.relplot(x='min_period', y='dist', kind='line', hue='foot', data=dfs,
                row='period')
plt.show()

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(pm, col='pos')
     .map(sns.kdeplot, 'pass', shade=True))

plt.show()


# wrap columns
g = (sns.FacetGrid(pm, col='pos', col_wrap=2)
     .map(sns.kdeplot, 'pass', shade=True))

# adding a title
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of No of Passes by Position')

# modifying options
g.set(xlim=(-5, 120))

g.set_xlabels('Passes')
g.set_ylabels('Density')

# saving
g.savefig(path.join(FIG_DIR, 'no_passes_by_position.png'))

#############
# shot charts
#############

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfs[['name', 'dist', 'foot', 'goal', 'x1', 'y1']].head(5)

dfs['x'] = dfs['x1']*115/100
dfs['y'] = (100 - dfs['y1'])*74/100

# shot data
g = sns.relplot(data=dfs, x='x', y='y', kind='scatter')
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)

map_img = mpimg.imread('./fig/soccer_field.png')

# scatter plot with field overlay
g = sns.relplot(data=dfs, x='x', y='y', kind='scatter')
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])

plt.show()

# how about a bit of jitter
dfs['xj'] = dfs['x'].apply(lambda x: x + random.gauss(0, 1))
dfs['yj'] = dfs['y'].apply(lambda x: x + random.gauss(0, 1))

g = sns.relplot(data=dfs, x='xj', y='yj', kind='scatter')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# putting it in a function
def shot_chart(df, **kwargs):
    g = sns.relplot(data=df, x='xj', y='yj', kind='scatter', **kwargs)
    g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
    g.despine(left=True, bottom=True)

    for ax in g.fig.axes:
        ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])

    return g

shot_chart(dfs, hue='goal', style='goal')
shot_chart(dfs, col='foot', hue='foot')

# and columns
teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
dfs = pd.merge(dfs, teams[['team_id', 'team']], how='left')

shot_chart(dfs, hue='goal', style='goal', col='team', height=3, col_wrap=4,
           s=10)

# now let's try a contour plot
g = (sns.FacetGrid(dfs, col='foot', hue='foot')
     .map(sns.kdeplot, 'x', 'y', alpha=0.5, shade=True)
     .add_legend())
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])

# add goal row, turn shading off
g = (sns.FacetGrid(dfs, col='foot', hue='foot')
     .map(sns.kdeplot, 'x', 'y', alpha=0.5)
     .add_legend())
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
