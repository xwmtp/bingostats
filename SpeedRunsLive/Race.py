import logging
from Utils import *
import re

versions = {
    'v9.3' : '09-06-2018',
    'v9.2' : '08-10-2016',
    'v9.1' : '02-07-2016',
    'v9'   : '09-04-2016',
    'v8.5' : '30-01-2016',
    'v8.4' : '13-12-2014',
    'v8.3' : '13-09-2014',
    'v?'   : '01-06-2011',
    'v2'   : '01-01-1990'
}

blacklist = [
    '219509', # scara's wr Kappa
    '100176'  # blackout ???
]

html_symbols = {
    '&quot;' : '"',
    '&amp;'  : '&',
    '&lt;'   : '<',
    '&gt;'   : '>'
}


class Race:


    def __init__(self, race_json, player_json, SRL_data, generate_board=True):

        self.id = race_json['id']
        self.goal = race_json['goal']
        self.date = dt.datetime.fromtimestamp(int(race_json['date'])).date()

        self.seed = self.get_seed(self.goal)
        self.type = self.get_type(self.goal)
        self.total_players = race_json['numentrants']

        self.time = dt.timedelta(seconds=player_json['time'])
        self.rank = player_json['place']
        self.points = int(player_json['newtrueskill'])
        self.comment = self.get_comment(player_json['message'])
        self.forfeit = self.rank > self.total_players
        self.dq = player_json['time'] == -2

        self.row_id = self.get_row_id(self.comment)

        if self.type in SRL_data.bingo_versions.keys() and self.row_id != 'blank' and generate_board:
            bingo_version = SRL_data.bingo_versions[self.type]
            if self.row_id != 'blank':
                self.row = bingo_version.get_row(int(self.seed), self.row_id)
            self.label = self._get_zl_label(SRL_data)
        else:
            self.row = []


    #def _get_row(self, id):
    #    if (id == 'BLANK') or (self.board == None):
    #        return []
    #    else:
    #        return self.board.row(id)


    def get_type(self, goal):
        self.is_bingo = False

        def get_version_date():

            for version, date in versions.items():
                version_date = dt.datetime.strptime(date, '%d-%m-%Y').date()
                if self.date >= version_date:
                    return version

        def find_version():
            return re.search(r'v\d+(\.(\d)+)*', goal)

        if self.id in blacklist:
            return 'blacklisted'

        if goal.startswith('http://www.speedrunslive.com/tools/oot-bingo'):
            if 'short' in goal:
                return 'short'
            if 'blackout' in goal:
                return 'blackout'
            self.is_bingo = True
            found_version = find_version()
            if found_version:
                return found_version.group()
            else:
                return get_version_date()

        if goal.startswith('http://www.buzzplugg.com/bryan/v9.2NoSaria/'):
            return 'no-saria'
        for name in {'v4', 'v5', 'v6', 'v7', 'v8'}:
            if name in goal.lower():
                return name.replace('.', '')
        if 'series' or 'championship' in goal:
            return 'ocs '

        return 'other'


    def get_seed(self,url):
        seed = re.search('seed=(\d)+', url)
        if seed:
            seed = seed.group()
        else:
            seed = '-----'
        digit = seed.replace('seed=', '')
        return digit

    def get_row_id(self, comment):

        def extract_row(comment):
            pattern = r'(^|\s)((((r(ow)?)|(c(ol)?))( )?(\d))|(tl(-| )?br)|(bl(-| )?tr))($|\s)'

            match = re.search(pattern, comment, re.IGNORECASE)
            if match:
                return match.group().lower().strip()
            else:
                return 'blank'

        regex_row = extract_row(comment)

        if regex_row == 'blank':
            return regex_row

        digit_match = re.search(r'\d', regex_row)
        if digit_match:
            digit = int(digit_match.group())
            if digit < 1 or digit > 5:
                logging.debug('FOUND WRONG ROW NUMBER IN COMMENT: ' + comment)
                return 'blank'
            if regex_row.startswith('r'):
                return 'row' + str(digit)
            else:
                return 'col' + str(digit)
        # tlbr or bltr
        else:
            row = regex_row.replace('-', '').replace(' ', '')
            return row

    def get_comment(self, comment):
        for name, symbol in html_symbols.items():
            comment = comment.replace(name, symbol)
        return comment



    def _get_zl_label(self, SRL_data):
        labels = [SRL_data.label_dict[goal] for goal in self.row]
        if not labels:
            return 'Blank'
        if 'child' in labels:
            label =  'Child ZL'
        elif 'rba' in labels:
            label = 'Deep RBA'
        else:
            label = 'No ZL'
        # light arrow special case
        if (('All 3 Elemental Arrows' in self.row) or ('Light Arrows' in self.row)) and (('Beat the Spirit Temple' in self.row) or ('Defeat Twinrova' in self.row)):
            label = 'No ZL'
            rest = [SRL_data.label_dict[goal] for goal in set(self.row) - {'All 3 Elemental Arrows', 'Light Arrows', 'Beat the Spirit Temple', 'Defeat Twinrova'}]
            for lab in ['rba', 'child']:
                if lab in rest:
                    label = lab
        # dins fire special case
        bit = ['Beat the Forest Temple', 'Defeat Phantom Ganon', 'Forest Medallion', 'All 4 Market area Skulltulas', "Frog's HP"]
        if ("Din's Fire" in self.row) and ([g for g in bit if g in self.row]):
            label = 'rba'
            rest = [SRL_data.label_dict[goal] for goal in set(self.row) - set(bit)]
            if 'child' in rest:
                label = 'child'
        return label