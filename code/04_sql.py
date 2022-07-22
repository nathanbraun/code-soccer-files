import pandas as pd
from os import path
import sqlite3

###############################################
# loading csvs and putting them in a sqlite db
###############################################

# only need to run this section once

# handle directories
DATA_DIR = './data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 'soccer-data.sqlite'))

# load csv data
player_match = pd.read_csv(path.join(DATA_DIR, 'player_match.csv'))
player = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
game = pd.read_csv(path.join(DATA_DIR, 'matches.csv'))
team = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# and write it to sql
player_match.to_sql('player_match', conn, index=False, if_exists='replace')
player.to_sql('player', conn, index=False, if_exists='replace')
game.to_sql('game', conn, index=False, if_exists='replace')
team.to_sql('team', conn, index=False, if_exists='replace')

#########
# Queries
#########
conn = sqlite3.connect(path.join(DATA_DIR, 'soccer-data.sqlite'))

# return entire player table
df = pd.read_sql(
    """
    SELECT *
    FROM player
    """, conn)
df.head()

# return specific columns from player table + rename on the fly
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, team, pos, foot
    FROM player
    """, conn)
df.head()

###########
# filtering
###########

# basic filter, only rows where team is MIA
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos, foot
    FROM player
    WHERE team = 'Japan'
    """, conn)
df.head()

# AND in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, team, pos, foot
    FROM player
    WHERE team = 'Japan' AND pos == 'MID'
    """, conn)
df.head()

# OR in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, team, pos, foot
    FROM player
    WHERE team = 'Japan' OR pos == 'GKP'
    """, conn)
df.head()

# IN in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos, foot
    FROM player
    WHERE pos IN ('DEF', 'MID')
    """, conn)
df.head()

# negation with NOT
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, team, pos, foot
    FROM player
    WHERE team NOT IN ('Japan', 'Iceland')
    """, conn)
df.head()

#########
# joining
#########

# no WHERE so fullcrossjoin
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team,
        team.grouping
    FROM player, team
    """, conn)
df.head(10)

# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.grouping
    FROM player, team
    """, conn)
df.head(10)

# n of rows
df.shape

# works when we add WHERE to filter after crossjoin
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team,
        team.grouping
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# add in team column to make clearer how it works
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.grouping
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head(10)

# adding a third table
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        team.team,
        team.city,
        team.grouping,
        player_match.*
    FROM player, team, player_match
    WHERE
        player.team = team.team AND
        player_match.player_id = player.player_id
    """, conn)
df.head()

# adding a third table - shorthand
df = pd.read_sql(
    """
    SELECT
        p.player_name as name,
        p.pos,
        t.team,
        t.city,
        t.grouping,
        pm.match_id,
        pm.pass
    FROM player AS p, team AS t, player_match AS pm
    WHERE
        p.team = t.team AND
        pm.player_id = p.player_id
    """, conn)
df.head()

# adding an additional filter
df = pd.read_sql(
    """
    SELECT
        p.player_name as name,
        p.pos,
        t.team,
        t.city,
        t.grouping,
        pm.match_id,
        pm.pass
    FROM player AS p, team AS t, player_match AS pm
    WHERE
        p.team = t.team AND
        pm.player_id = p.player_id AND
        p.pos == 'FWD'
    """, conn)
df.head()

###########
# LIMIT/TOP
###########

# SELECT *
# FROM player
# LIMIT 5

# SELECT TOP 5 *
# FROM player

df = pd.read_sql(
    """
    SELECT DISTINCT ref, ref2
    FROM game
    """, conn)
df.head()

# UNION
# SUBQUERIES
# LEFT, RIGHT, OUTER JOINS

# SELECT *
# FROM <left_table>
# LEFT JOIN <right_table> ON <left_table>.<common_column> = <right_table>.<common_column>

df = pd.read_sql(
    """
    SELECT a.*, b.min, b.pass, b.shot, b.goal
    FROM
        (SELECT match_id, label, home as team, away as opp, player_id, player_name
        FROM game, player
        WHERE game.home = player.team_id
        UNION
        SELECT match_id, label, home as team, away as opp, player_id, player_name
        FROM game, player
        WHERE game.away = player.team_id) AS a
    LEFT JOIN player_match AS b ON a.match_id = b.match_id AND a.player_id = b.player_id
    """, conn)


# Kudryahsov id = 101647
df.query("player_id == 101647")

df.loc[df['player_name'] == 'L. Messi']

# game = pd.read_sql(
#     """
#     SELECT *
#     FROM game
#     """
#     , conn)

# game.loc[[11, 0, 1, 2, 3]]

# game.query("home == 'GB'")
