##############
# basic python
##############

##########################
# how to read this chapter
##########################
1 + 1

##########
# comments
##########

# print the result of 1 + 1
print(1 + 1)

###########
# variables
###########

goals_scored = 2

goals_scored
3*goals_scored

goals_scored = goals_scored + 1
goals_scored

####################
# types of variables
####################

keeper_saves = 12  # int
ball_speed_kmh = 96.5  # float

starting_fwd = 'Lionel Messie'
description = "It's a goal"

type(starting_fwd)

type(keeper_saves)

player_description = f'{description} by {starting_fwd}!'
player_description

# string methods
'gooaaaaal'.upper()

'Christiano Ronaldo, Man U'.replace('Man U', 'Real Madrid')

####################################
# How to figure things out in Python
####################################
'lionel messie'.capitalize()

'  lionel messie'
'lionel messie'

'  lionel messie'.lstrip()

#######
# bools
#######
team1_goals = 2
team2_goals = 1

# and these are all bools:
team1_won = team1_goals > team2_goals
team2_won = team1_goals < team2_goals
teams_tied = team1_goals == team2_goals
teams_did_not_tie = team1_goals != team2_goals

type(team1_won)
teams_did_not_tie

# error because test for equality is ==, not =
# teams_tied = (team1_goals = team2_goals)  # commented out since it throws an error

shootout = (team1_goals > 3) and (team2_goals > 3)
at_least_one_good_team = (team1_goals > 3) or (team2_goals > 3)
you_guys_are_bad = not ((team1_goals > 1) or (team2_goals > 1))
meh = not (shootout or at_least_one_good_team or you_guys_are_bad)

###############
# if statements
###############
if team1_won:
  message = "Nice job team 1!"
elif team2_won:
  message = "Way to go team 2!!"
else:
  message = "must have tied!"

message

#################
# container types
#################

# lists
roster_list = ['ruben dias', 'gabriel jesus', 'riyad mahrez']

roster_list[0]
roster_list[0:2]
roster_list[-2:]

# dicts
roster_dict = {'CB': 'ruben dias',
               'CF': 'gabriel jesus',
               'RW': 'riyad mahrez'}

roster_dict['CB']
roster_dict['LW'] = 'raheem sterling'

pos = 'RW'
roster_dict[pos]

# unpacking
cb, dm = ['ruben dias', 'fernandinho']

cb = 'ruben dias'
dm = 'fernandinho'

# gives an error - n of variables doesn't match n items in list
# cb, dm = ['ruben dias', 'fernandinho', 'riyad mahrez']  # commented out w/ error

#######
# loops
#######

# looping over a list
roster_list = ['ruben dias', 'gabriel jesus', 'riyad mahrez']

roster_list_upper = ['', '', '']
i = 0
for player in roster_list:
    roster_list_upper[i] = player.title()
    i = i + 1

roster_list_upper

for x in roster_dict:
    print(f"position: {x}")

for x in roster_dict:
   print(f"position: {x}")
   print(f"player: {roster_dict[x]}")

for x, y in roster_dict.items():
    print(f"position: {x}")
    print(f"player: {y}")

################
# comprehensions
################

# lists
roster_list
roster_list_proper = [x.title() for x in roster_list]
roster_list_proper

roster_list_proper_alt = [y.title() for y in roster_list]

type([x.title() for x in roster_list])
[x.title() for x in roster_list][:2]

roster_last_names = [full_name.split(' ')[1] for full_name in roster_list]
roster_last_names

full_name = 'ruben dias'
full_name.split(' ')
full_name.split(' ')[1]

roster_r_only = [
    x for x in roster_list if x.startswith('r')]

roster_r_only

'ruben dias'.startswith('r')
'gabriel jesus'.startswith('r')
'riyad mahrez'.startswith('r')

roster_r_only_title = [
    x.title() for x in roster_list if x.startswith('r')]

roster_r_only_title

# dicts
salary_per_player = {
    'ruben dias': 6000000, 'gabriel jesus': 4680000, 'riyad mahrez': 6240000}

salary_m_per_upper_player = {
    name.upper(): salary/1000000 for name, salary in salary_per_player.items()}

salary_m_per_upper_player

sum([1, 2, 3])

sum([salary for _, salary in salary_per_player.items()])

###########
# functions
###########
len(['ruben dias', 'gabriel jesus', 'riyad mahrez'])

n_goals = len(['ruben dias', 'gabriel jesus', 'riyad mahrez'])
n_goals

4 + len(['ruben dias', 'gabriel jesus', 'riyad mahrez'])

def ejected(nyellow, nred):
    """
    multi line strings in python are between three double quotes

    it's not required, but the convention is to put what the fn does in one of
    these multi line strings (called "docstring") right away in function

    this function takes number of yellow and red cards and returns a bool
    indicating whether the player is ejected
    """
    return (nred >= 1) or (nyellow >= 2)

ejected(1, 0)

# this gives an error: nyellow is only defined inside ejected
# print(nyewllow)

def ejected_noisy(nyellow, nred):
    """
    this function takes number of yellow and red cards and returns a bool
    indicating whether the player is ejected

    it also prints out nyellow
    """
    print(nyellow)  # works here since we're inside fn
    return (nred >= 1) or (nyellow >= 2)

ejected_noisy(0, 1)

# side effects
def is_player_on_team(player, team):
    """
    take a player string and team list and check whether the player is on team

    do this by adding the player to the team, then returning True if the player
    shows up 2 or more times
    """
    team.append(player)
    return team.count(player) >= 2

roster_list = ['ruben dias', 'gabriel jesus', 'riyad mahrez']
is_player_on_team('eric garcia', roster_list)

roster_list
is_player_on_team('eric garcia', roster_list)

roster_list

# function arguments
## Positional vs Keyword Arguments

ejected(1, 0)
ejected(0, 1)  # order matters!

ejected?

ejected(nred=0, nyellow=1)  # keyword arguments

ejected(1, nred=0)

# error: keyword arguments can't come before positional arguments
# ejected(nred=0, 1)

## Default Values for Arguments

# error: leaving off an argument
# ejected(1)  

def ejected_wdefault(nyellow, nred=0):
    """
    this function takes number of yellow and red cards and returns a bool
    indicating whether the player is ejected
    """
    return (nred >= 1) or (nyellow >= 2)


ejected_wdefault(2)

# error: leaving out required argument
# ejected_wdefault(nred=0)

# error: 
# def ejected_wdefault_wrong(nyellow=0, nred):
#     """
#     this function takes number of yellow and red cards and returns a bool
#     indicating whether the player is ejected
#     """
#     return (nred >= 1) or (nyellow >= 2)

# error: can't put key word argument before positional
# make_player_stats_dict(nred=1, "Lionel Messie", 1, 2)

#####################################
# functions that take other functions
#####################################

def do_to_list(working_list, working_fn, desc):
    """
    this function takes a list, a function that works on a list, and a
    description

    it applies the function to the list, then returns the result along with
    description as a string
    """

    value = working_fn(working_list)

    return f'{desc} {value}'

def last_elem_in_list(working_list):
    """
    returns the last element of a list.
    """
    return working_list[-1]

positions = ['FWD', 'MID', 'D', 'GK']

do_to_list(positions, last_elem_in_list, "last element in your list:")
do_to_list([1, 2, 4, 8], last_elem_in_list, "last element in your list:")

do_to_list(positions, len, "length of your list:")

do_to_list([2, 3, 7, 1.3, 5], lambda x: 3*x[0], "first element in your list times 3 is:")

# normally imports like this would be at the top of the file
import os

os.cpu_count()

from os import path

# change this to the location of your data
DATA_DIR = '/Users/nathan/code-soccer-files/data'
path.join(DATA_DIR, 'shots.csv')
os.path.join(DATA_DIR, 'shots.csv')  # alt if we didn't want to import path
