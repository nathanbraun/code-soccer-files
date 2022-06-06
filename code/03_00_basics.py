from os import path
import pandas as pd

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

##############
# Loading data
##############
shots = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

type(shots)

##################################
# DataFrame methods and attributes
##################################
shots.head()

shots.columns

shots.shape

#################################
# Working with subsets of columns
#################################
# A single column
shots['name'].head()

type(shots['name'])

shots['name'].to_frame().head()
type(shots['name'].to_frame().head())

# Multiple columns
shots[['name', 'foot', 'goal', 'period']].head()

type(shots[['name', 'foot', 'goal', 'period']])

# commented out because it throws an error
# shots['name', 'foot', 'goal', 'period'].head() 

##########
# Indexing
##########
shots[['name', 'foot', 'goal', 'period']].head()

shots.set_index('shot_id').head()

# Copies and the inplace argument
shots.head()  # note: shot_id not the index, even though we just set it

shots.set_index('shot_id', inplace=True)
shots.head()  # now shot_id is index

# alternate to using inplace, reassign adp
# reload shots with default 0, 1, ... index
shots = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
shots = shots.set_index('shot_id')
shots.head()  # now shot_id is index

shots.reset_index().head()

#############################
# Indexes keep things aligned
#############################
shots_ot = shots.loc[((shots['period'] == 'E1') |
                     (shots['period'] == 'E2')),
                     ['name', 'goal', 'period']]
shots_ot.head()

shots_ot.sort_values('name', inplace=True)
shots_ot.head()

# assigning a new column
shots_ot['foot'] = shots['foot']
shots_ot.head()

# has the same index as adp_rbs and shots['foot']
shots['foot'].head()

#################
# Outputting data
#################
shots_ot.to_csv(path.join(DATA_DIR, 'shots_ot.csv'))

shots_ot.to_csv(path.join(DATA_DIR, 'shots_ot_no_index.csv'), index=False)

