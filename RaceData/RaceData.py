from Utils import *
from RaceData.Player import Player
from RaceData.Race import Race
import dateutil.parser as dp




def get_player(name, include_betas=False):
    if name == '':
        return

    srl_json = readjson(f'http://api.speedrunslive.com/pastraces?player={name}&pageSize=1500')
    racetime_user_json = readjson(f'http://localhost:8000/autocomplete/user?term={name}')
    def find_racetime_user_id(name, results):
        for user in results:
            if name.lower() == user['name'].lower():
                return user['url'].replace('/user/', '')
        for user in results:
            if name.lower() == user['twitch_name'].lower():
                return user['url'].replace('/user/', '')

    racetime_user_id = find_racetime_user_id(name, racetime_user_json['results'])
    if srl_json or racetime_user_json:
        player = Player(name)
        if srl_json:
            player.races += parse_srl_races(name, srl_json, include_betas)
        if racetime_user_id:
            racetime_json = readjson(f'http://localhost:8000/user/{racetime_user_id}/races/data?show_entrants=true')
            player.races += parse_racetime_races(name, racetime_json, include_betas)

        player.print_goals()
        return player






    # else:
    #     json = readjson(f'https://www.speedrun.com/api/v1/users?lookup={name}')
    #     if json['data'] != []:
    #         new_name = json['data'][0]['names']['international']
    #         if new_name.lower() != name.lower():
    #             logging.debug(f'Found alternative name {new_name}')
    #             return self.get_player(new_name)

def parse_srl_races(name, json, include_betas):
    results = []
    for race in json['pastraces']:
        if race['game']['abbrev'] == 'oot':
            for entrant in race['results']:
                if entrant['player'].lower() == name.lower():
                    race_info = srl_race_json_to_dict(race,entrant)
                    race_obj = Race(race_info, include_betas) #todo make it not necessary for Race to get include_betas
                    results.append(race_obj)
    races = [result for result in results if not result.dq]
    logging.debug(f'Parsed {len(races)} SRL races')
    return races

def parse_racetime_races(name, json, include_betas):
    results = []
    for race in json['races']:
        if race['name'].split('/')[0] == 'oot':
            for entrant in race['entrants']:
                if entrant['user']['name'].lower() == name.lower():
                    race_info = racetime_race_json_to_dict(race, entrant)
                    race_obj = Race(race_info, include_betas)
                    results.append(race_obj)
    races = [result for result in results if not result.dq]
    logging.debug(f'Parsed {len(races)} racetime.gg races')
    return races


def srl_race_json_to_dict(race, entrant):
    dict = {}
    dict['id'] = race['id']
    dict['goal'] = race['goal']
    dict['date'] = race['date']
    dict['goal'] = race['goal']
    dict['num_entrants'] = race['numentrants']
    dict['recordable'] = True
    dict['time'] = entrant['time']
    dict['forfeit'] = dict['time'] == -1
    dict['dq'] = dict['time'] == -2
    dict['rank'] = entrant['place']
    dict['points'] = entrant['newtrueskill']
    dict['comment'] = entrant['message']
    return dict

def racetime_race_json_to_dict(race, entrant):
    dict = {}
    dict['id'] = race['name']
    dict['goal'] = race['goal']
    dict['date'] = race['ended_at']
    if dict['date']:
        dict['date'] = '1541293253'#str(dp.parse(dict['date']).strftime('%s')) # from iso to unix
    else:
        dict['date'] = '0'
    dict['goal'] = race['goal']['name']
    dict['num_entrants'] = race['entrants_count']
    if race['info']:
        dict['goal'] += f" {race['info']}"
    dict['recordable'] = race['recordable']
    dict['time'] = entrant['finish_time']
    if dict['time']:
        dict['time'] = '11325'#str(dp.parse(dict['time']).strftime('%s')) # from iso to unix
    else:
        dict['time'] = '0'
    dict['forfeit'] = entrant['status']['value'] == 'dnf'
    dict['dq'] = entrant['status']['value'] == 'dq'
    dict['rank'] = entrant['place']
    dict['points'] = entrant['score'] if entrant['score'] else 0
    dict['comment'] = entrant['comment'] if entrant['comment'] else 0
    return dict
