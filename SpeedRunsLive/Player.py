from SpeedRunsLive.Race import Race
from Utils import *
import numpy as np


class Player:

    def __init__(self, name, json, SRL_data):
        self.name = name
        self.short_goal_dict = convert_to_dict('short_goal_names.txt')

        if name == '' or name == '-1':
            self.races = []
        else:
            self.races = self.get_races(json['pastraces'], SRL_data)


    def get_races(self, json, SRL_data):
        results = []
        for race in json:
            for entrant in race['results']:
                if entrant['player'].lower() == self.name.lower():
                    self.name = entrant['player']
                    race_obj = Race(race, entrant, SRL_data)
                    results.append(race_obj)
        return [result for result in results if not result.dq]


    def select_races(self, n=-1, type = 'bingo', sort = 'best', forfeits=False, span = None):
        # type
        if type == 'bingo':
            races = [race for race in self.races if race.is_bingo]
        else:
            races = [race for race in self.races if race.type == type]

        # time span
        if span != None:
            races = [race for race in races if (race.date >= span.start) and (race.date <= span.end)]

        # forfeits
        if not forfeits:
            races = [race for race in races if not race.forfeit]


        # sorting
        if sort == 'best':
            races = sorted(races, key=lambda r: r.time)
        elif sort == 'latest':
            races = sorted(races, key=lambda r: r.date, reverse=True)


        if n==-1:
            n = len(races)
        return races[:n]


    def get_pb(self, type = 'bingo'):
        race = self.select_races(type=type)[0]
        return race.time

    def get_goal_counts(self, type = 'bingo', span = None):
        races = self.select_races(type=type, span = span)

        dict = {}
        for race in races:
            if race.row != []:
                for goal in race.row:
                    if goal in dict.keys():
                        dict[goal] = dict[goal] + 1
                    else:
                        dict[goal] = 1

        goal_counts = dict.items()
        goal_counts = sorted(goal_counts, key=lambda x: x[1], reverse=True)
        return goal_counts


    def get_versions(self):
        races = self.select_races(sort='latest')
        versions = set([race.type for race in races])
        versions = sorted([version for version in versions if version != 'v?'], reverse=True)
        return versions

    def get_latest_version(self):
        versions = self.get_versions()
        if versions == []:
            return 'all'
        else:
            return versions[0]



    def get_pandas_table(self, type = 'bingo'):
        races = self.select_races(type = type)
        rows = [race.row for race in races]

        df_dict = {
            'Time'    : [convert_to_human_readable_time(race.time.total_seconds())[1] for race in races],
            'Date'    : [race.date for race in races],
            'Type'    : [race.type for race in races],
            'Rank'    : [int(r.rank) for r in races],
            'Entrants': [int(r.total_players) for r in races],
            'SRL-id'      : [race.id for race in races],
        }
        # goals
        for i in range(5):
            goals = [self.short_goal_dict[r[i]].lower() if len(r) == 5 else '' for r in rows]
            df_dict['Goal' + str(i+1)] = goals

        df_dict['Comment'] = [race.comment for race in races]

        df = pd.DataFrame(df_dict)
        df = df[list(df_dict.keys())]
        return df