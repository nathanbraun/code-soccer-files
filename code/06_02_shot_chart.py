import pandas as pd
import random
from pandas import DataFrame
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from os import path

pd.options.mode.chained_assignment = None
%matplotlib qt

DATA_DIR = './data'

# load data
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfm = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# process data
# note: figured this out through trial and error - makes coordinates roughly
# field shaped going left to right
dfs = pd.merge(dfs, dfm[['match_id', 'home_team', 'away_team']], how='left')
dfs = pd.merge(dfs, dft[['team_id', 'team']], how='left')

dfs['x'] = dfs['x1']*120/100
dfs['y'] = (100 - dfs['y1'])*75/100

#############
# shot charts
#############

# book picks up here
dfs[['name', 'dist_m', 'foot', 'goal', 'x', 'y']].head(5)

# shot data
g = sns.relplot(data=dfs, x='x', y='y', kind='scatter')
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)

import matplotlib.image as mpimg
map_img = mpimg.imread('./fig/soccer_field.png')

# scatter plot with field overlay
g = sns.relplot(data=dfs, x='x', y='y', kind='scatter', size=5)
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 120, 0, 75])

# how about a bit of jitter
dfs['xj'] = dfs['x'].apply(lambda x: x + random.gauss(0, 1))
dfs['yj'] = dfs['y'].apply(lambda x: x + random.gauss(0, 1))

g = sns.relplot(data=dfs, x='xj', y='yj', kind='scatter')
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 120, 0, 75])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# putting it in a function
def shot_chart(df, **kwargs):
    g = sns.relplot(data=df, x='xj', y='yj', kind='scatter', **kwargs)
    g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
    g.despine(left=True, bottom=True)

    for ax in g.fig.axes:
        ax.imshow(map_img, zorder=0, extent=[0, 120, 0, 75])

    return g

# kwargs
def add2(num1, num2):  
    return num1 + num2

def add2_flexible(num1, num2, **kwargs):
    return num1 + num2

add2_flexible(num1=4, num2=5, num3=1, num4=4)

# commented out because it throws an error
# add2(num1=4, num2=5, num3=1)  

shot_chart(dfs, hue='goal', style='goal', s=10)
shot_chart(dfs, row='foot', hue='foot', s=10)

# and columns
shot_chart(dfs, hue='goal', style='goal', col='team', height=3, col_wrap=4,
           s=10)

# now let's try a contour plot
g = (sns.FacetGrid(dfs, row='foot', hue='foot', col='goal')
     .map(sns.kdeplot, 'x', 'y', alpha=0.5))
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 120, 0, 75])

# turn shading off - by team
g = (sns.FacetGrid(dfs, col='team', col_wrap=4, height=2, hue='team')
     .map(sns.kdeplot, 'x', 'y', alpha=0.5))
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[0, 120, 0, 75])
