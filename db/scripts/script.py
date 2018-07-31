import requests, enums, json
from joblib import Parallel, delayed

def get_schedule():
    r = requests.get('http://data.nba.net/data/10s/prod/v1/2017/schedule.json');
    #error handle here
    return r.json()['league']['standard']

def get_lawler(game, points):
    if game['seasonStageId'] == 2:
        if int(game['hTeam']['score']) < points and int(game['vTeam']['score']) < points:
            return enums.lawler_rv.NO_LAWLER  


        plays, plays_len = get_plays(game, points)
        if plays_len == -1:
            return enums.lawler_rv.NO_LAWLER

        first_to_x = enums.team.NOLAWLER
        winner = enums.team.HOME if int(game['hTeam']['score']) > int(game['vTeam']['score']) else enums.team.AWAY
        first_to_x = search_for_play(plays, 0, plays_len, points)

        if first_to_x == winner:
            return enums.lawler_rv.TRUE_LAWLER
        elif first_to_x != enums.team.NOLAWLER and first_to_x != winner:
            return enums.lawler_rv.FALSE_LAWLER

        return enums.lawler_rv.NO_LAWLER
    else:
        return enums.lawler_rv.NO_LAWLER


def get_plays(game, points):
    period = get_period(points)
    pbp_data = {
        'date': game['startDateEastern'],
        'gameId': game['gameId'],
        'period': period
    }

    pbp_rv = requests.get('http://data.nba.net/data/10s/prod/v1/%(date)s/%(gameId)s_pbp_%(period)s.json' % pbp_data)
    if pbp_rv.status_code == requests.codes.ok:
        plays = pbp_rv.json()['plays'] 
        plays_len = len(plays) - 1 
    else:
        return [], -1

    while int(plays[plays_len]['hTeamScore']) < points and int(plays[plays_len]['vTeamScore']) < points:
        if period == 4 and int(plays[plays_len]['hTeamScore']) != int(plays[plays_len]['vTeamScore']):
            return [], -1
        period += 1
        pbp_data = {
            'date': game['startDateEastern'],
            'gameId': game['gameId'],
            'period': period
        }

        pbp_rv = requests.get('http://data.nba.net/data/10s/prod/v1/%(date)s/%(gameId)s_pbp_%(period)s.json' % pbp_data)
        if pbp_rv.status_code == requests.codes.ok:
            plays = pbp_rv.json()['plays'] 
            plays_len = len(plays) - 1
        else:
            return [], -1

    while int(plays[0]['hTeamScore']) > points and int(plays[0]['vTeamScore']) > points:
        period -= 1
        pbp_data = {
            'date': game['startDateEastern'],
            'gameId': game['gameId'],
            'period': period
        }
        pbp_rv = requests.get('http://data.nba.net/data/10s/prod/v1/%(date)s/%(gameId)s_pbp_%(period)s.json' % pbp_data)
        if pbp_rv.status_code == requests.codes.ok:
            plays = pbp_rv.json()['plays'] 
            plays_len = len(plays) - 1
        else:
            return [], -1

    return plays, plays_len

def get_period(points): 
    if points >= 88:
        return 4
    elif points >= 66:
        return 3
    elif points >= 44:
        return 2
    else:
        return 1 

def search_for_play(plays, l, r, points):
    while l <= r:
        mid = l + int((r-l)/2)
        home_score = int(plays[mid]['hTeamScore'])
        away_score = int(plays[mid]['vTeamScore'])

        if away_score >= points and home_score < points:
            return enums.team.AWAY
        elif away_score < points and home_score >= points:
            return enums.team.HOME
        elif away_score >= points and home_score >= points:
            r = mid - 1
        else:
            l = mid + 1 
    else:
        return enums.team.NOLAWLER

def main():
    nba_db = {}
    schedule = get_schedule()

    # game = schedule[170]

    # rv = get_lawler(game, 58)
    # # print(schedule.index(game))
    # print(rv)

    # for game in schedule:
    #     rv = get_lawler(game, 64)
    #     print(schedule.index(game))
    #     print(rv)

    #https://stackoverflow.com/questions/17167297/convert-this-python-dictionary-into-json-format (for later)

    for i in range(100,104):
        results = Parallel(n_jobs=64, backend="threading")(delayed(get_lawler)(game, i) for game in schedule)
        rv = list(map(sum, zip(*results)))

        nba_db[i] = [{"year": "17-18", "season": "regular", "data": {"true_lawler": rv[0], "total_lawler": rv[1]}}]
    
    r = json.dumps(nba_db, indent=4)
    print(r)



if __name__ == '__main__':
    main()
