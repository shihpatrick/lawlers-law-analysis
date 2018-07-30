import requests
from joblib import Parallel, delayed

# global var
NOLAWLER = -1
HOMETEAM = 0
AWAYTEAM = 1
BADVAR = 2

def get_schedule():
    r = requests.get('http://data.nba.net/data/10s/prod/v1/2017/schedule.json');
    #error handle here
    return r.json()['league']['standard']

def get_lawler(game, points):
    if game['seasonStageId'] == 2:
        pbp_data = {
            'date': game['startDateEastern'],
            'gameId': game['gameId'],
            'period': 4
        }
        #error handle here
        pbp_rv = requests.get('http://data.nba.net/data/10s/prod/v1/%(date)s/%(gameId)s_pbp_%(period)s.json' % pbp_data)

        winner = HOMETEAM if int(game['hTeam']['score']) > int(game['vTeam']['score']) else AWAYTEAM

        plays = pbp_rv.json()['plays']
        first_to_x = NOLAWLER

        for play in plays:
            home_score = int(play['hTeamScore'])
            away_score = int(play['vTeamScore'])

            if away_score >= points and home_score < points:
                first_to_x = AWAYTEAM
                break
            elif away_score < points and home_score >= points:
                first_to_x = HOMETEAM
                break
            elif away_score >= points and home_score >= points:
                #both team hit points, check 3d qtr
                first_to_x = BADVAR
                break

        if first_to_x == winner or first_to_x == BADVAR:
            return [1,1]
        elif first_to_x != NOLAWLER and first_to_x != winner:
            return [0,1]

        return [0,0]
    else:
        return [0,0]



def main():
    nba_db = {}
    schedule = get_schedule()
    for i in range(90,101):
        results = Parallel(n_jobs=32, backend="threading")(delayed(get_lawler)(game, i) for game in schedule)
        rv = list(map(sum, zip(*results)))
        nba_db[i] = rv
    
    print(nba_db)
    

if __name__ == '__main__':
    main()







