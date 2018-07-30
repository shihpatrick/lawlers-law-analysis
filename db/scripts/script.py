import requests

r = requests.get('http://data.nba.net/data/10s/prod/v1/2017/schedule.json');

# global var
HOMETEAM = 0
AWAYTEAM = 0

schedule = r.json()['league']['standard']

game = schedule[120]

if game['seasonStageId'] == 2:
	pbp_data = {
		'date': game['startDateEastern'],
		'gameId': game['gameId'],
		'period': '4'
	}

	pbp_rv = requests.get('http://data.nba.net/data/10s/prod/v1/%(date)s/%(gameId)s_pbp_%(period)s.json' % pbp_data)

	pbp = pbp_rv.json()
