"""
Answers to the end of chapter exercises for Python chapter.

Questions with written (not code) answers are inside triple quotes.
"""

###############################################################################
# 2.1
###############################################################################
"""
a) `_throwaway_data`. Valid. Python programmers often start variables with `_`
   if they're throwaway or temporary, short term variables.
b) `n_shots`. Valid.
c) `1st_half`. Not valid. Can't start with a number.
d) `shotsOnGoal`. Valid, though convention is to split words with `_`, not
    camelCase.
e) `wc_2018_champion`. Valid. Numbers OK as long as they're not in the first
    spot
f) `player position`. Not valid. No spaces
g) `@home_or_away`. Not valid. Only non alphanumeric character allowed is `_`
h) `'num_penalties'`. Not valid. A string (wrapped in quotes), not a variable
    name. Again, only non alphanumeric character allowed is `_`
"""

###############################################################################
# 2.2
###############################################################################
match_minutes = 45
match_minutes = match_minutes + 45
match_minutes = match_minutes + 5

match_minutes # 95

###############################################################################
# 2.3
###############################################################################
def commentary(player, play):
    return f'{player} with the {play}!'

commentary('Messi', 'goal')

###############################################################################
# 2.4
###############################################################################
"""
It's a string method, so what might `islower()` in the context of a string?
I'd say it probably returns whether or not the string is lowercase.

A function "is *something*" usually returns a yes or no answer (is it
something or not), which would mean it returns a boolean.

We can test it like:
"""

'lionel messi'.islower()  # should return True
'Lionel Messi'.islower()  # should return False

###############################################################################
# 2.5
###############################################################################
def is_oconnell(player):
    return player.replace("'", '').lower() == 'jack oconnell'

is_oconnell('lionel messi')
is_oconnell("Jack O'Connell")
is_oconnell("JACK OCONNELL")

###############################################################################
# 2.6
###############################################################################

# Write a function `a_lot_of_goals` that takes in a number (e.g. 0, 2, or 6) and
# returns a string `'6 is a lot of goals!` if the number is >= 4 or `"2 is not
# that many goals"` otherwise.

def a_lot_of_goals(goals):
    if goals >= 4:
        return f'{goals} is a lot of goals!'
    else:
        return f'{goals} is not that many goals'

a_lot_of_goals(3)
a_lot_of_goals(7)

###############################################################################
# 2.7
###############################################################################
roster = ['ruben dias', 'gabriel jesus', 'riyad mahrez']

roster[0:2]
roster[:2]
roster[:-1]
[x for x in roster if x != 'riyad mahrez']
[x for x in roster if x in ['ruben dias', 'gabriel jesus']]

###############################################################################
# 2.8
###############################################################################
shot_info = {'shooter': 'Robert Lewandowski', 'foot': 'right', 'went_in':
    False}

# a
shot_info['shooter'] = 'Cristiano Ronaldo'
shot_info

# b
def toggle_foot(info):
    if info['foot'] == 'right':
        info['foot'] = 'left'
    else:
        info['foot'] = 'right'
    return info

shot_info
toggle_foot(shot_info)

###############################################################################
# 2.9
###############################################################################
"""
a) No. `'is_pk'` hasn't been defined.
b) No, `shooter` is a variable that hasn't been defined, the key is
`'shooter'`.
c) Yes.
"""

###############################################################################
# 2.10
###############################################################################
roster = ['ruben dias', 'gabriel jesus', 'riyad mahrez']

# a
for x in roster:
  print(x.split(' ')[-1])

# b
{player: len(player) for player in roster}

###############################################################################
# 2.11
###############################################################################
roster_dict = {'CB': 'ruben dias',
               'CF': 'gabriel jesus',
               'RW': 'riyad mahrez',
               'LW': 'raheem sterling'}

# a
[pos for pos in roster_dict]

# b
[player for _, player in roster_dict.items()
    if player.split(' ')[-1][0] in ['j', 'm']]

###############################################################################
# 2.12
###############################################################################
# a
def mapper(my_list, my_function):
    return [my_function(x) for x in my_list]

# b
match_minutes = [95, 92, 91, 91, 97, 95]

mapper(match_minutes, lambda x: x - 90)
