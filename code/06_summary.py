import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from os import path
import matplotlib.image as mpimg

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathanbraun/fantasymath/code-soccer-files/data'
FIG_DIR = '/Users/nathanbraun/fantasymath/code-soccer-files/fig'

###############
# distributions
###############

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

###############
# summary stats
###############

# book picks up here:

# quantile function and describe

df['dist'].quantile(.9)
df[['dist', 'time']].describe()

##########
# plotting
##########

# basic displot
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 60))
plt.show()

# all on one line
g = sns.FacetGrid(df).map(sns.kdeplot, 'dist', shade=True)
plt.show()

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'dist', shade=True))

# density plot of standard points by goal or not
g = (sns.FacetGrid(df, hue='goal')
     .map(sns.kdeplot, 'dist', shade=True)
     .add_legend())
plt.show()

# density plot of distance by goal and body part
g = (sns.FacetGrid(df, hue='goal', col='foot', height=2)
     .map(sns.kdeplot, 'dist', shade=True)
     .add_legend())
g.set(xlim=(0, 50))
plt.show()

#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type

# TODO: figure out something for reshaping into same columns
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

pm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

# passes vs player rank
sns.relplot(x='pass', y='player_rank', data=pm)
plt.show()

# passes vs player rank - by position
sns.relplot(x='pass', y='player_rank', hue='pos', data=pm)
plt.show()

# passes vs player rank - by position and team
sns.relplot(x='pass', y='player_rank', hue='pos', col='team', data=pm,
            col_wrap=4)

#############
# correlation
#############
pm = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))

['name', 'team', 'min', 'shot', 'goal', 'assist', 'player_id', 'match_id',
 'date', 'pass', 'pass_accurate', 'tackle', 'accel', 'counter', 'opportunity',
 'keypass', 'own_goal', 'interception', 'smart', 'clearance', 'cross',
 'air_duel', 'air_duel_won', 'gk_leave_line', 'gk_save_attempt', 'throw',
 'corner', 'pos', 'side', 'player_rank', 'started']

pm[['min', 'shot', 'goal', 'pass', 'pass_accurate', 'player_rank']].corr()

# scatter plot of 0.1489 correlation
g = sns.relplot(x='pass_accurate', y='player_rank', data=pm)
plt.show()

# scatter plot of 0.99 correlation
g = sns.relplot(x='pass', y='pass_accurate', data=dft)
plt.show()

########################
# line plots with python
########################

# let's look at scoring by week

# minor processing
score_long = pd.merge(score_long, matches[['match_id', 'group', 'venue', 'gameweek']])
score_long.loc[score_long['gameweek'] == 0, 'gameweek'] = 4

# by group
g = sns.relplot(x='gameweek', y='score', kind='line', data=score_long,
                hue='group', col='group', col_wrap=4)

# by team (just the line)
g = sns.relplot(x='gameweek', y='score', kind='line', data=score_long,
                hue='team', col='group', col_wrap=4)

# shot distance by foot/minute
df['pmin'] = df['time'] // 60
g = sns.relplot(x='pmin', y='dist', kind='line', hue='foot', data=df, row='period')
plt.show()

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(df, col='foot', hue='goal')
     .map(sns.kdeplot, 'dist', shade=True))

# wrap columns
g = (sns.FacetGrid(df, col='foot', hue='goal', col_wrap=2)
     .map(sns.kdeplot, 'dist', shade=True))

# adding a title
g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Shot Distances by Body Part, Made')

# modifying options
g.set(xlim=(-5, 40))

g.set_xlabels('Ft')
g.set_ylabels('Density')

# saving
g.savefig(path.join(FIG_DIR, 'shot_dist_foot_made.png'))

#############
# shot charts
#############

df['y1'] = 100 - df['y1']

df['x'] = df['x1']*115/100
df['y'] = df['y1']*74/100

map_img = mpimg.imread(path.join(FIG_DIR, 'field_coordinates_cropped.png'))

# scatter plot with field overlay
g = sns.relplot(data=df, x='x1', y='y1', kind='scatter', s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# how about a bit of jitter
df['x_j'] = np.random.uniform(df['x1'] - 0.5, df['x1'] + 0.5)*115/100
df['y_j'] = np.random.uniform(df['y1'] - 0.5, df['y1'] + 0.5)*74/100

g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# add some hue
g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter',
                hue='goal', style='goal')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# and columns
g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', col='opportunity',
                hue='goal', style='goal')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# counter?
g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', col='counter',
                hue='goal', style='goal')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# finally, teams
teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
df = pd.merge(df, teams[['team_id', 'team']], how='left')

g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', col='team',
                col_wrap=4, hue='goal', style='goal', height=2, aspect=115/74)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
g.savefig(path.join(FIG_DIR, 'shot_chart_teams.png'))

plt.show()


# now let's try a contour plot
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'x', 'y', alpha=0.5)
     .add_legend())
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
plt.show()

# same thing, rows and columns
g = (sns.FacetGrid(df, col='foot', hue='foot', row='goal')
     .map(sns.kdeplot, 'x', 'y', alpha=0.5)
     .add_legend())
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 115, 0, 74])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()
