import requests
import json
from pandas import DataFrame, Series
import pandas as pd

fpl_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
fpl_resp = requests.get(fpl_url)

# note - i saved a snapshot of the FPL API data above and included it in the
# repo under ./data/json/fpl.json

# can use if you want
# pro - data will match what's in the book, avoid errors if anything's changed
# con - saved data, not "real" api

# live data from API
fpl_json = fpl_resp.json()  

# uncomment the lines below if you want to use that snapshot vs connecting to
# the live API

with open('./data/json/fpl.json') as f:
    fpl_json = json.load(f)

fpl_json
fpl_json.keys()

type(fpl_json['teams'])

fpl_json['teams'][0]

df_teams = DataFrame(fpl_json['teams'])

# reordering columns so more interesting ones are at beginning - cosmetic
df_teams = df_teams[['name', 'short_name', 'id', 'code', 'draw', 'form',
    'loss', 'played', 'points', 'position', 'strength', 'team_division',
    'unavailable', 'win', 'strength_overall_home', 'strength_overall_away',
    'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
    'strength_defence_away', 'pulse_id']]

df_teams.head()

# match data

type(fpl_json['elements'])
len(fpl_json['elements'])

fpl_json['elements'][0]

df_players = DataFrame(fpl_json['elements'])

df_players = df_players[['first_name', 'second_name', 'team', 'id',
    'chance_of_playing_next_round', 'chance_of_playing_this_round', 'code',
    'cost_change_event', 'cost_change_event_fall', 'cost_change_start',
    'cost_change_start_fall', 'dreamteam_count', 'element_type', 'ep_next',
    'ep_this', 'event_points', 'form', 'in_dreamteam', 'news', 'news_added',
    'now_cost', 'photo', 'points_per_game', 'selected_by_percent', 'special',
    'squad_number', 'status', 'team_code', 'total_points', 'transfers_in',
    'transfers_in_event', 'transfers_out', 'transfers_out_event', 'value_form',
    'value_season', 'web_name', 'goals_scored', 'assists', 'clean_sheets',
    'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
    'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index',
    'influence_rank', 'influence_rank_type', 'creativity_rank',
    'creativity_rank_type', 'threat_rank', 'threat_rank_type',
    'ict_index_rank', 'ict_index_rank_type',
    'corners_and_indirect_freekicks_order',
    'corners_and_indirect_freekicks_text', 'direct_freekicks_order',
    'direct_freekicks_text', 'penalties_order', 'penalties_text', 'minutes',
    'yellow_cards', 'red_cards']]

df_players.sample(5)

match_url = 'https://fantasy.premierleague.com/api/fixtures/'
match_resp = requests.get(match_url)

match_json = match_resp.json()

# uncomment the lines below if you want to use a saved snapshot of match data
# vs connecting to the live API

# with open('./data/json/match.json') as f:
#     match_json = json.load(f)

match0 = match_json[0]
match0

match_cols = [key for key in match0 if key != 'stats']
df_match = DataFrame(match_json)[match_cols]
df_match[['id', 'team_a', 'team_h', 'team_a_score', 'team_h_score',
    'kickoff_time']].head()

# player data
# uses fpl_json, which we loaded above
