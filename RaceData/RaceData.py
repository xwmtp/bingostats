from Utils import *
from RaceData.Player import Player
from BingoBoards.BingoVersions import BINGO_VERSIONS
from BingoBoards.BingoVersion import ROW_INDICES
from Definitions import ALIASES, is_api_supported_version, is_pregenerated_version
from RaceData.ParseRace import parse_srl_race, parse_racetime_race
import math



def get_player(player_data):
    if player_data:
        player =  Player(player_data['name'], player_data['races'], player_data['include_betas'])
        return player

# name to look up, possible to add an existing player to add the races to
def load_player_data(name, include_betas=False):
    if name == '':
        return
    player_data = lookup_player_data(name, include_betas)
    for aliases in ALIASES:
        if any(a for a in aliases if a.lower() == name.lower()):
            lookup_names = [a for a in aliases if a.lower() != name.lower()]
            for alias in lookup_names:
                player_data = lookup_player_data(alias, include_betas=include_betas, player_data=player_data)
    return player_data

def lookup_player_data(name, include_betas=False, player_data=None):
    logging.debug(f"Looking up name {name}...")
    srl_json = readjson(f'https://api.speedrunslive.com/pastraces?player={name}&pageSize=1500')
    racetime_user_json = readjson(f'https://racetime.gg/autocomplete/user?term={name}')

    racetime_user_id = find_racetime_user_id(name, racetime_user_json['results'])
    if srl_json or racetime_user_json:
        if not player_data:
            logging.debug(f'Creating new player data for name {name}')
            player_data = {'name' : name, 'include_betas' : include_betas, 'races' : []}
        if srl_json:
            player_data['races'] += parse_srl_races(name, srl_json)
        if racetime_user_id:
            player_data['races'] += parse_racetime_races(name, racetime_user_id)

        add_goals(player_data['races'])
    return player_data


def find_racetime_user_id(name, results):
    for user in results:
        if name.lower() == user['name'].lower():
            return user['url'].replace('/user/', '')
    for user in results:
        if name.lower() == user['twitch_name'].lower():
            return user['url'].replace('/user/', '')



def parse_srl_races(name, json):
    results = []
    for race in json['pastraces']:
        if race['game']['abbrev'] == 'oot':
            for entrant in race['results']:
                if entrant['player'].lower() == name.lower():
                    results.append(parse_srl_race(race, entrant))
    races = [r for r in results if not r['dq'] and r['recordable']]
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
                        race_dict = parse_racetime_race(race, entrant)
                        results.append(race_dict)
        page += 1
        num_pages = json['num_pages']
    races = [r for r in results if not r['dq'] and r['recordable']]
    logging.debug(f'Parsed {len(races)} racetime.gg races')
    return races



def add_goals(races):
    bingos = [r for r in races if r['bingo']]
    versions = set([r['type'] for r in bingos])
    for version in versions:
        version_bingos = [r for r in bingos if r['type'] == version]
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
        if bingo['row_id'] != 'blank':
            bingo['row'] = version_boards.get_row(int(bingo['seed']), bingo['row_id'])

def add_api_goals(version, races):
    logging.debug(f'Looking up {len(races)} boards for version {version}')
    seeds = [r['seed'] for r in races]
    goal_data = readjson(f"https://scaramangado.de/oot-bingo-api?version={version.replace('b', 'beta')}&seeds={','.join(seeds)}&mode=normal")
    if goal_data:
        boards = goal_data['boards']
        for i in range(len(races)):
            bingo = races[i]
            if bingo['row_id'] != 'blank':
                indices = ROW_INDICES[bingo['row_id']]
                bingo['row'] = [boards[i]['goals'][j] for j in indices]








