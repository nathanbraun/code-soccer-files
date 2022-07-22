"""
Answers to the end of chapter exercises for SQL chapter.

Note: this assumes you've already created/populated the SQL database as
outlined in the book and ./code/04_sql.py.
"""
import pandas as pd
from os import path
import sqlite3

DATA_DIR = './data'

conn = sqlite3.connect(path.join(DATA_DIR, 'soccer-data.sqlite'))

###############################################################################
# 4.1
###############################################################################
df  = pd.read_sql(
    """
    SELECT
        date, name AS player, team.team, goal, shot, pass
    FROM
        player_match, team
    WHERE
        team.team = player_match.team AND
        team.grouping = 'C'
    """, conn)

###############################################################################
# 4.2
###############################################################################
df  = pd.read_sql(
    """
    SELECT
        date, name AS player, t.team, goal, shot, pass, height, weight
    FROM
        player_match AS pm,
        team AS t,
        player AS p
    WHERE
        t.team = pm.team AND
        t.grouping = 'C' AND
        pm.player_id = p.player_id
    """, conn)

