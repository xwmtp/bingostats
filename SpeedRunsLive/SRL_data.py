import logging
from Utils import *
from SpeedRunsLive.Player import Player
from BingoBoards.BingoVersion import BingoVersion


class SRL:



    def __init__(self):
        self.bingo_versions = {
            'v9.2' : BingoVersion('v92'),
            'v9.3' : BingoVersion('v93')
        }

        self.short_goal_dict = convert_to_dict('short_goal_names.txt')
        self.label_dict = convert_to_dict('zl_labels.txt')

    def get_player(self, name, from_file=False):

        if from_file:
            json = readjson_file('./data/races_' + name + '.txt')
        else:
            json = readjson('http://api.speedrunslive.com/pastraces?player=' + name + '&pageSize=1000')

        if json:
            logging.info('Loading player ' + name)
            return Player(name, json, self)
        else:
            json = readjson('https://www.speedrun.com/api/v1/users?lookup=' + name)
            if json['data'] != []:
                logging.debug(json['data'])
                new_name = json['data'][0]['names']['international']
                if new_name.lower() != name.lower():
                    return self.get_player(new_name)

