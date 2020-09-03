import datetime as dt

class Race:

    def __init__(self, race_info):
        self.platform = race_info['platform']
        self.id = race_info['id']
        self.goal = race_info['goal']
        self.total_players = race_info['num_entrants']
        self.date = dt.datetime.strptime(race_info['date'], '%Y-%m-%d').date()
        self.time = dt.timedelta(seconds=race_info['time'])

        self.seed = race_info['seed']
        self.type = race_info['type']

        self.is_bingo = race_info['bingo']
        self.is_beta = race_info['beta']
        self.forfeit = race_info['forfeit']
        self.dq = race_info['dq'] == 'True'
        self.recordable = race_info['recordable']
        self.finished = not self.forfeit and not self.dq

        self.rank = race_info['rank']
        self.points = int(race_info['points'])
        self.comment = race_info['comment']

        self.row_id = race_info['row_id']
        self.row = [] # gets filled later




    def is_type(self, type):
        if self.type == type:
            return True
        if self.is_beta and self.type.startswith(type):
            return True
        return False

    def get_type(self, shorten_betas=False):
        type = self.type
        if shorten_betas and self.is_beta:
            type = '.'.join(self.type.split('.')[:3])
        return type


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