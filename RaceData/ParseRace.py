from Definitions import VERSIONS, BLACKLIST
from Utils import *
import re
import datetime as dt
import isodate



def parse_srl_race(race, entrant):
    dict = {}
    dict['platform'] = 'srl'
    dict['id'] = race['id']
    dict['goal'] = race['goal']
    dict['date'] = str(dt.datetime.fromtimestamp(int(race['date'])).date())
    dict['num_entrants'] = race['numentrants']
    dict['recordable'] = 'True'
    dict['time'] = entrant['time'] #seconds
    dict['forfeit'] = entrant['time'] == -1
    dict['dq'] = entrant['time'] == -2
    dict['rank'] = entrant['place']
    dict['points'] = entrant['newtrueskill']
    dict['comment'] = entrant['message']
    return add_bingo_data(dict)

def parse_racetime_race(race, entrant):
    dict = {}
    dict['platform'] = 'racetime'
    dict['id'] = race['name'].replace('oot/','')
    dict['goal'] = race['goal']
    dict['date'] = race['ended_at']
    if dict['date']:
        dict['date'] = str(isodate.parse_date(dict['date']))
    else:
        dict['date'] = str(dt.date(1970, 1, 1))
    dict['goal'] = race['goal']['name']
    dict['num_entrants'] = race['entrants_count']
    if race['info']:
        dict['goal'] += f" {race['info']}"
    dict['recordable'] = race['recordable']
    dict['time'] = entrant['finish_time']
    if dict['time']:
        dict['time'] = isodate.parse_duration(dict['time']).seconds
    else:
        dict['time'] = 0
    dict['forfeit'] = entrant['status']['value'] == 'dnf'
    dict['dq'] = entrant['status']['value'] == 'dq'
    dict['rank'] = entrant['place']
    dict['points'] = entrant['score'] if entrant['score'] else 0
    dict['comment'] = entrant['comment'] if entrant['comment'] else ''
    return add_bingo_data(dict)

def add_bingo_data(dict):
    dict['comment'] = parse_comment(dict['comment'])
    type, is_bingo, is_beta = parse_type_info(dict['goal'], dict['date'], dict['id'])
    dict['type'] = type
    dict['bingo'] = is_bingo
    dict['beta'] = is_beta
    dict['seed'] = parse_seed(dict['goal'])
    dict['row_id'] = parse_row_id(dict['comment'])
    dict['row'] = [] # gets filled later
    return dict


def parse_type_info(goal, date, race_id):
    goal = goal.lower()
    version = parse_version(goal, date)
    type, is_bingo = parse_type(goal, version, race_id)
    if 'beta' in type:
        is_beta = True
        type = type.replace('beta', 'b')
    else:
        is_beta = False

    return type, is_bingo, is_beta


def parse_type(goal, version, race_id):
    if race_id in BLACKLIST:
        return 'blacklisted', False

    if 'speedrunslive.com/tools/oot-bingo' in goal or f'ootbingo.github.io/bingo/{version}/bingo.html' in goal:
        for mode in ['short', 'long', 'blackout', 'black out', '3x3', 'anti', 'double', 'bufferless', 'child', 'jp', 'japanese', 'bingo-j']:
            if mode in goal:
                return mode, False
        return version, True

    if 'http://www.buzzplugg.com/bryan/v9.2nosaria/' in goal:
        return 'no-saria', False
    for name in {'v4', 'v5', 'v6', 'v7', 'v8'}:
        if name in goal:
            return name.replace('.', ''), False
    if 'series' in goal or 'championship' in goal:
        return 'ocs', False
    return 'other', False


def parse_version(goal, date):
    found_version = re.search(r'v\d+(\.(\d)+)*|(beta)\d+(\.\d+)*(-[A-Za-z]*)?', goal)
    if found_version:
        return found_version.group()
    date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    for version, version_date in VERSIONS.items():
        version_date = dt.datetime.strptime(version_date, '%d-%m-%Y').date()
        if date >= version_date:
            return version


def parse_seed(url):
    seed = re.search('seed=(\d)+', url)
    if seed:
        seed = seed.group()
    else:
        seed = '-----'
    digit = seed.replace('seed=', '')
    return digit


def parse_row_id(comment):
    regex_row = extract_row(comment)
    if regex_row == 'blank':
        return regex_row
    digit_match = re.search(r'\d', regex_row)
    if digit_match: # row or col
        digit = int(digit_match.group())
        if digit < 1 or digit > 5:
            logging.debug(f'FOUND WRONG ROW NUMBER IN COMMENT: {comment}')
            return 'blank'
        if regex_row.startswith('r'):
            return 'row' + str(digit)
        else:
            return 'col' + str(digit)
    else: # tlbr or bltr
        row = regex_row.replace('-', '').replace(' ', '')
        return row


def extract_row(comment):
    row_pattern = '((((r(ow)?)|(c(ol)?))( )?(\d))|(tl(-| )?br)|(bl(-| )?tr)){1}'
    pattern = rf'(?:^|\s|[^\w]){row_pattern}(?:$|[^\d])'

    match = re.search(pattern, comment, re.IGNORECASE)
    if match:
        return match.groups()[0].lower().strip()
    else:
        return 'blank'


def parse_comment(comment):
    html_symbols = {
        '&quot;': '"',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>'
    }
    comment = str(comment)
    for name, symbol in html_symbols.items():
        comment = comment.replace(name, symbol)
    return comment
