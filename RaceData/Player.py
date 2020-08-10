from Utils import *
import logging

SHORT_GOAL_NAMES = convert_to_dict('short_goal_names.txt', to_lower=True)

class Player:

    def __init__(self, name, include_betas=False):
        self.name = name
        self.include_betas = include_betas
        self.races = []

    def select_races(self, n=-1, type = 'bingo', sort = 'best', forfeits=False, span = None):
        # type
        if type == 'bingo':
            races = [race for race in self.races if race.is_bingo]
        else:
            races = [race for race in self.races if race.type == type]
        # betas
        if not self.include_betas:
            races = [race for race in races if not race.is_beta]
        # time span
        if span != None:
            races = [race for race in races if (race.date >= span.start) and (race.date <= span.end)]
        # forfeits
        if not forfeits:
            races = [race for race in races if race.finished]
        else:
            races = [race for race in races if not race.dq]
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

    def get_favorite_row(self):
        rows = [race.row_id for race in self.races if race.row_id != 'blank']
        if rows != []:
            return max(set(rows), key=rows.count)

    def get_favorite_goal(self, version='bingo'):
        if version=='bingo':
            row_lists = [race.row for race in self.races]
        else:
            row_lists = [race.row for race in self.races if race.row if race.type==version]
        rows = [goal for row in row_lists for goal in row]
        if rows != []:
            return max(set(rows), key=rows.count)

    def get_average(self, n=10, type = 'bingo'):
        latest_races = self.select_races(n=n, sort='latest', type = type)
        times = [r.time for r in latest_races]
        forfeits = self.get_forfeit_count(n, type, latest_races)
        if len(times) > 0:
            logging.debug([str(time) for time in times])
            return sum(times, dt.timedelta(0)) / len(times), forfeits
        else:
            return '-', 0

    def get_median(self, n=10, type = 'bingo'):
        latest_races = self.select_races(n=n, sort='latest', type = type)
        times = [r.time for r in latest_races]
        forfeits = self.get_forfeit_count(n, type, latest_races)
        print('normal med:')
        return self.calc_median(times), forfeits

    def calc_median(self, times):
        if len(times) > 0:
            times = sorted(times)
            print([str(t) for t in times])
            mid = int(len(times) / 2)
            if len(times) % 2 == 0:
                median = (times[mid - 1] + times[mid]) / 2
            else:
                median = times[mid]
            return median
        else:
            return '-'

    # penalizes forfeits
    def get_effective_median(self, n=10):
        all_latest_races = self.select_races(n=n, sort='latest', forfeits=True, type='bingo')
        forfeits = len([r for r in all_latest_races if r.forfeit])
        plain_median, _ = self.get_median(n=(len(all_latest_races) - forfeits))
        times = [plain_median * 1.25 if r.forfeit else r.time for r in all_latest_races]
        print('effective med:')
        effective_median = self.calc_median(times)
        return effective_median

    def get_forfeit_count(self, n, type, races):
        """Get the amount of forfeits in a list of races that happened in the last n. Assumes races is sorted by latest date."""
        if races == []:
            return 0
        oldest_race = races[-1]
        all_races = self.select_races(-1, type, sort='latest', forfeits=True)
        forfeits = 0
        for race in all_races:
            if race.forfeit:
                forfeits += 1
            if race.id == oldest_race.id:
                return forfeits
        logging.warning(f'Never foud race with id {race.id} for get_forfeit_count!')
        return forfeits

    def get_pandas_table(self, type = 'bingo'):
        races = self.select_races(type = type)
        rows = [race.row for race in races]

        df_dict = {
            'Time'    : [convert_to_human_readable_time(race.time.total_seconds())[1] for race in races],
            'Date'    : [race.date for race in races],
            'Type'    : [race.type.replace('beta', 'b') for race in races],
            'Rank'    : [f'{r.rank}/{r.total_players}' for r in races],
            'Race-id'  : [race.id for race in races],
        }
        # goals
        for i in range(5):
            goals = [SHORT_GOAL_NAMES[r[i].lower()] if len(r) == 5 else '' for r in rows]
            if any([goal != '' for goal in goals]):
                df_dict['Goal' + str(i+1)] = goals

        df_dict['Comment'] = [race.comment for race in races]

        df = pd.DataFrame(df_dict)
        df = df[list(df_dict.keys())]
        df = df.sort_values('Date', ascending=False)
        return df

    ### DEBUG
    def print_goals(self):
        for race in self.races:
            if race.is_bingo:
                logging.debug(f'Bingo goal: {race.goal} | Type: {race.type} | id: {race.id}')
        for race in self.races:
            if not race.is_bingo:
                logging.debug(f'Non-bingo goal: {race.goal} | Type: {race.type} | id: {race.id}')