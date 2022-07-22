"""
Answers to the end of chapter exercises for Summary Stats and Visualization
chapter.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import path

DATA_DIR = './data'

dftm = pd.read_csv(path.join(DATA_DIR, 'team_match.csv'))

###############################################################################
# 6.1
###############################################################################

# 6.1a
g = (sns.FacetGrid(dftm)
     .map(sns.kdeplot, 'pass', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Passes')
g.savefig('./solutions-to-exercises/6-1a.png')

# Now modify your plot to show the distribution of passes by whether the team
# won. Do it (b) as separate colors on the same plot, and (c) as separate
# plots.

# 6.1b
g = (sns.FacetGrid(dftm, hue='win')
    .map(sns.kdeplot, 'pass', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Passes by Win/Loss B')
g.savefig('./solutions-to-exercises/6-1b.png')

# 6.1c
g = (sns.FacetGrid(dftm, col='win')
    .map(sns.kdeplot, 'pass', shade=True))
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Distribution of Passes by Win/Loss C')
g.savefig('./solutions-to-exercises/6-1c.png')

# 6.1d

g = (sns.FacetGrid(dftm, col='win', hue='win')
    .map(sns.kdeplot, 'pass', shade=True))
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Distribution of Passes by Win/Loss D')
g.savefig('./solutions-to-exercises/6-1d.png')


# 6.1e
g = (sns.FacetGrid(dftm, col='team', col_wrap=6)
    .map(sns.kdeplot, 'pass', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Passes by Team')
g.savefig('./solutions-to-exercises/6-1e.png')

###############################################################################
# 6.2
###############################################################################
# 6.2a 
g = sns.relplot(x='pass', y='pass_opp', data=dftm)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Passes vs Opponent Passes')
g.savefig('./solutions-to-exercises/6-2a.png')

# 6.2b
dftm[['pass', 'pass_opp']].corr()

