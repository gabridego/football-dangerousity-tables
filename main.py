import os
import requests
import json
from argparse import ArgumentParser

import pandas as pd
from tqdm import trange
import pymongo


def parse_args():
    parser = ArgumentParser(description="Team dangerousity collector")
    parser.add_argument('-a', '--auth-endpoint', type=str, required=True,
                        help='URL of authentication endpoint')
    parser.add_argument('-u', '--auth-username', type=str, required=True,
                        help='Username to access authentication endpoint')
    parser.add_argument('-p', '--auth-password', type=str, required=True,
                        help='Password to access authentication endpoint')
    parser.add_argument('-m', '--match-endpoint', type=str, required=True,
                        help='URL of endpoint of match statistics')
    parser.add_argument('-d', '--mongodb-uri', type=str, nargs='?',
                        default='mongodb://mongo:27017/',
                        help='URI of mongodb host')
    parser.add_argument('-c', '--calendar-path', type=str, nargs='?',
                        default='data/calendar.json',
                        help='Path to JSON file containing match information')
    parser.add_argument('-o', '--home-output-path', type=str, nargs='?',
                        default='out/home_dangerousity.csv',
                        help='Output path for the file containing dangerousity in home matches')
    parser.add_argument('-w', '--away-output-path', type=str, nargs='?',
                        default='out/away_dangerousity.csv',
                        help='Output path for the file containing dangerousity in away matches')
    return parser.parse_args()


def verify_args(args):
    if '{id}' not in args.match_endpoint:
        raise ValueError("Match endpoint must contain {id}")

        
def get_dangerousity_value(l, id_team):
    for x in l:
        if x['id_team'] == id_team:
            return x['value'][0]
    return None


def main(args):
    calendar_path = args.calendar_path
    
    with open(calendar_path) as f:
        calendar = json.load(f)
    
    # retrieve matches and teams id
    ## "home_team,away_team" --> match_id
    match_ids = {}
    ## team --> team_id
    teams_ids = {}

    for match_date in calendar['matchDate']:
        for match in match_date['match']:
            match_ids[f"{match['homeContestantName']},{match['awayContestantName']}"] = match['id']
            if match['homeContestantName'] not in teams_ids:
                teams_ids[match['homeContestantName']] = match['homeContestantId']
            if match['awayContestantName'] not in teams_ids:
                teams_ids[match['awayContestantName']] = match['awayContestantId']

    ## team names
    teams = sorted(teams_ids.keys())
    
    # ensure all matches and teams are retrieved
    assert len(match_ids) == 380
    assert len(teams) == 20
    
    # get access token
    access_token = requests.post(args.auth_endpoint,
                                 json={"username": args.auth_username,
                                       "password": args.auth_password}).json()['access_token']
    
    # create output directory, if not existing
    out_path = os.path.dirname(args.home_output_path)
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.dirname(args.away_output_path)
    os.makedirs(out_path, exist_ok=True)
    
    # connect to mongodb
    client = pymongo.MongoClient(args.mongodb_uri)
    db = client["tactical"]
    
    # initialize tables
    home_dang_df = pd.DataFrame(index=teams, columns=teams)
    away_dang_df = pd.DataFrame(index=teams, columns=teams)
    
    for i in trange(len(teams) - 1, desc="home team"):
        for j in trange(i + 1, len(teams), desc="away team", leave=False):
            # home matches
            home_team, away_team = teams[i], teams[j]

            # request data for home match
            home_match_id = match_ids[f"{home_team},{away_team}"]
            data = requests.get(args.match_endpoint.format(id=home_match_id),
                                headers={'Authorization': f'Bearer {access_token}'},
                                params={'agg': 'Yes'}).json()['team']['tactical']

            for k in data.keys():
                # store in data in collection
                if len(data[k]) > 0:
                    db[k].insert_many(data[k])

                if k == 'team_attack_maneuvre_absolute_dangerousity':
                    # get entries for maneuvre dangerousity
                    maneuvre_dangerousity = data[k]
                    # store dangerousity of home and away teams (in the two tables)
                    home_dang_df.at[home_team, away_team] = get_dangerousity_value(maneuvre_dangerousity,
                                                                                   teams_ids[home_team])
                    away_dang_df.at[away_team, home_team] = get_dangerousity_value(maneuvre_dangerousity,
                                                                                   teams_ids[away_team])

            # same but for away matches
            home_team, away_team = teams[j], teams[i]

            away_match_id = match_ids[f"{home_team},{away_team}"]
            data = requests.get(args.match_endpoint.format(id=away_match_id),
                                headers={'Authorization': f'Bearer {access_token}'},
                                params={'agg': 'Yes'}).json()['team']['tactical']

            for k in data.keys():
                # store in data in collection
                if len(data[k]) > 0:
                    db[k].insert_many(data[k])

                if k == 'team_attack_maneuvre_absolute_dangerousity':
                    # get entries for maneuvre dangerousity
                    maneuvre_dangerousity = data[k]
                    # store dangerousity of home and away teams (in the two tables)
                    home_dang_df.at[home_team, away_team] = get_dangerousity_value(maneuvre_dangerousity,
                                                                                   teams_ids[home_team])
                    away_dang_df.at[away_team, home_team] = get_dangerousity_value(maneuvre_dangerousity,
                                                                                   teams_ids[away_team])
            
    # save output files
    home_dang_df.to_csv(args.home_output_path)
    away_dang_df.to_csv(args.away_output_path)


if __name__ == "__main__":
    args = parse_args()
    verify_args(args)
    main(args)
