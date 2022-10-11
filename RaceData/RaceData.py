from Utils import *
from RaceData.Player import Player
from RaceData.Race import Race
from BingoBoards.BingoVersions import BINGO_VERSIONS
from BingoBoards.BingoVersion import ROW_INDICES
from Definitions import ALIASES, is_api_supported_version, is_pregenerated_version
import datetime as dt
import isodate
import math



# name to look up, possible to add an existing player to add the races to
def get_player(name, include_betas=False):
    if name == '':
        return
    player = lookup_player(name, include_betas)
    for aliases in ALIASES:
        if any(a for a in aliases if a.lower() == name.lower()):
            lookup_names = [a for a in aliases if a.lower() != name.lower()]
            for alias in lookup_names:
                player = lookup_player(alias, include_betas=include_betas, player=player)
    return player

def lookup_player(name, include_betas=False, player=None):
    logging.debug(f"Looking up name {name}...")
    #srl_json = readjson(f'https://api.speedrunslive.com/pastraces?player={name}&pageSize=1500')
    racetime_user_json = readjson(f'https://racetime.gg/autocomplete/user?term={name}')

    def find_racetime_user_id(name, results):
        for user in results:
            if name.lower() == user['name'].lower():
                return user['url'].replace('/user/', '')
        for user in results:
            if name.lower() == user['twitch_name'].lower():
                return user['url'].replace('/user/', '')

    racetime_user_id = find_racetime_user_id(name, racetime_user_json['results'])
    if racetime_user_json: # or srl_json:
        if not player:
            logging.debug(f'Creating now player object for name {name}')
            player = Player(name, include_betas)
        # if srl_json:
        #     player.races += parse_srl_races(name, srl_json)
        if racetime_user_id:
            player.races += parse_racetime_races(name, racetime_user_id)

        add_goals(player.races)
    return player


def add_goals(races):
    bingos = [r for r in races if r.is_bingo]
    versions = set([r.type for r in bingos])
    for version in versions:
        version_bingos = [r for r in bingos if r.type == version]
        # version has been pre generated
        if is_pregenerated_version(version):
            add_pregenerated_goals(version, version_bingos)
        # use api
        elif is_api_supported_version(version):
            add_api_goals(version, version_bingos)

def add_pregenerated_goals(version, races):
    logging.debug(f'Using {len(races)} pre-generated boards for version {version}')
    version_boards = BINGO_VERSIONS[version]
    for bingo in races:
        if bingo.row_id != 'blank':
            bingo.row = version_boards.get_row(int(bingo.seed), bingo.row_id)

def add_api_goals(version, races):
    logging.debug(f'Looking up {len(races)} boards for version {version}')
    seeds = [r.seed for r in races]
    goal_data = readjson(f"https://scaramangado.de/oot-bingo-api?version={version.replace('b', 'beta')}&seeds={','.join(seeds)}&mode=normal")
    if goal_data:
        boards = goal_data['boards']
        for i in range(len(races)):
            bingo = races[i]
            if bingo.row_id != 'blank':
                indices = ROW_INDICES[bingo.row_id]
                bingo.row = [boards[i]['goals'][j] for j in indices]






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
