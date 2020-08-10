from Utils import *
from RaceData.Player import Player
from RaceData.Race import Race
import datetime as dt
import isodate
import math




def get_player(name, include_betas=False):
    if name == '':
        return

    srl_json = readjson(f'https://api.speedrunslive.com/pastraces?player={name}&pageSize=1500')
    racetime_user_json = readjson(f'https://racetime.gg/autocomplete/user?term={name}')
    def find_racetime_user_id(name, results):
        for user in results:
            if name.lower() == user['name'].lower():
                return user['url'].replace('/user/', '')
        for user in results:
            if name.lower() == user['twitch_name'].lower():
                return user['url'].replace('/user/', '')

    racetime_user_id = find_racetime_user_id(name, racetime_user_json['results'])
    if srl_json or racetime_user_json:
        player = Player(name, include_betas)
        if srl_json:
            player.races += parse_srl_races(name, srl_json)
        if racetime_user_id:
            player.races += parse_racetime_races(name, racetime_user_id)

        return player

def parse_srl_races(name, json):
    results = []
    for race in json['pastraces']:
        if race['game']['abbrev'] == 'oot':
            for entrant in race['results']:
                if entrant['player'].lower() == name.lower():
                    race_info = srl_race_json_to_dict(race,entrant)
                    race_obj = Race(race_info)
                    results.append(race_obj)
    races = [result for result in results if not result.dq and result.recordable]
    logging.debug(f'Parsed {len(races)} SRL races')
    return races

def parse_racetime_races(name, id):
    results = []
    page = 1
    num_pages = math.inf
    while page <= num_pages:
        json = readjson(f'https://racetime.gg/user/{id}/races/data?show_entrants=true&page={page}')
        for race in json['races']:
            if race['name'].split('/')[0] == 'oot':
                for entrant in race['entrants']:
                    if entrant['user']['name'].lower() == name.lower():
                        race_info = racetime_race_json_to_dict(race, entrant)
                        race_obj = Race(race_info)
                        #debug (add copies of races with different rows)
                        #from BingoBoards.BingoVersion import ROW_IDS
                        #if race_obj.type == 'v9.5' or race_obj.type == 'v9.3':
                        #    for r in ROW_IDS:
                        #        race_info['comment'] = r
                        #        results.append(Race(race_info))
                        results.append(race_obj)
        page += 1
        num_pages = json['num_pages']
    races = [result for result in results if not result.dq and result.recordable]
    logging.debug(f'Parsed {len(races)} racetime.gg races')
    return races

def srl_race_json_to_dict(race, entrant):
    dict = {}
    dict['platform'] = 'srl'
    dict['id'] = race['id']
    dict['goal'] = race['goal']
    dict['date'] = dt.datetime.fromtimestamp(int(race['date'])).date()
    dict['num_entrants'] = race['numentrants']
    dict['recordable'] = True
    dict['time'] = dt.timedelta(seconds=entrant['time'])
    dict['forfeit'] = entrant['time'] == -1
    dict['dq'] = entrant['time'] == -2
    dict['rank'] = entrant['place']
    dict['points'] = entrant['newtrueskill']
    dict['comment'] = entrant['message']
    return dict

def racetime_race_json_to_dict(race, entrant):
    dict = {}
    dict['platform'] = 'racetime'
    dict['id'] = race['name'].replace('oot/','')
    dict['goal'] = race['goal']
    dict['date'] = race['ended_at']
    if dict['date']:
        dict['date'] = isodate.parse_date(dict['date'])
    else:
        dict['date'] = dt.date(1970, 1, 1)
    dict['goal'] = race['goal']['name']
    dict['num_entrants'] = race['entrants_count']
    if race['info']:
        dict['goal'] += f" {race['info']}"
    dict['recordable'] = race['recordable']
    dict['time'] = entrant['finish_time']
    if dict['time']:
        dict['time'] = isodate.parse_duration(dict['time'])
    else:
        dict['time'] = dt.timedelta(seconds=0)
    dict['forfeit'] = entrant['status']['value'] == 'dnf'
    dict['dq'] = entrant['status']['value'] == 'dq'
    dict['rank'] = entrant['place']
    dict['points'] = entrant['score'] if entrant['score'] else 0
    dict['comment'] = entrant['comment'] if entrant['comment'] else ''
    return dict
