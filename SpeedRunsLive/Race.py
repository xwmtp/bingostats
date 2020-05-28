import logging
from Definitions import VERSIONS, BLACKLIST
from Utils import *
import re


html_symbols = {
    '&quot;' : '"',
    '&amp;'  : '&',
    '&lt;'   : '<',
    '&gt;'   : '>'
}


class Race:


    def __init__(self, race_json, player_json, SRL_data, include_betas=False, generate_board=True):

        self.id = race_json['id']
        self.goal = race_json['goal']
        self.date = dt.datetime.fromtimestamp(int(race_json['date'])).date()

        self.seed = self.get_seed(self.goal)
        self.type = self.get_type(self.goal, include_betas)

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
        else:
            self.row = []


    def get_type(self, goal, include_betas):
        goal = goal.lower()
        # 'normal' bingo
        self.is_bingo = False

        def get_version():
            found_version = re.search(r'v\d+(\.(\d)+)*|(beta)\d+(\.\d+)*(-[A-Za-z]*)?', goal)
            if found_version:
                return found_version.group()

            for version, date in VERSIONS.items():
                version_date = dt.datetime.strptime(date, '%d-%m-%Y').date()
                if self.date >= version_date:
                    return version


        if self.id in BLACKLIST:
            return 'blacklisted'

        version = get_version()

        if 'speedrunslive.com/tools/oot-bingo' in goal or f'ootbingo.github.io/bingo/{version}/bingo.html' in goal:
            for mode in ['short', 'long', 'blackout', 'black out', '3x3', 'anti', 'double', 'bufferless', 'child', 'jp', 'japanese', 'bingo-j']:
                if mode in goal.lower():
                    return mode
            # only mark betas as 'bingo' when include_betas is true
            if (include_betas or not 'beta' in version):
                self.is_bingo = True
            return version

        if 'http://www.buzzplugg.com/bryan/v9.2nosaria/' in goal:
            return 'no-saria'
        for name in {'v4', 'v5', 'v6', 'v7', 'v8'}:
            if name in goal:
                return name.replace('.', '')
        if 'series' in goal or 'championship' in goal:
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
            row_pattern = '((((r(ow)?)|(c(ol)?))( )?(\d))|(tl(-| )?br)|(bl(-| )?tr)){1}'
            pattern = rf'(?:^|\s|[^\w]){row_pattern}(?:$|[^\d])'

            match = re.search(pattern, comment, re.IGNORECASE)
            if match:
                return match.groups()[0].lower().strip()
            else:
                return 'blank'

        regex_row = extract_row(comment)

        if regex_row == 'blank':
            return regex_row

        digit_match = re.search(r'\d', regex_row)
        if digit_match:
            digit = int(digit_match.group())
            if digit < 1 or digit > 5:
                logging.debug(f'FOUND WRONG ROW NUMBER IN COMMENT: {comment}')
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



    # currently not in use
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