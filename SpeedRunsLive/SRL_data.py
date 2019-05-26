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

        self.players = []

        self.short_goal_dict = convert_to_dict('short_goal_names.txt')
        self.label_dict = convert_to_dict('zl_labels.txt')

    def get_player(self, name, from_file=False):

        if name == '':
            return Player('', None, None) # the 'empty' player

        match = [player for player in self.players if name.lower() == player.name.lower()]
        if len(match) > 0:
            logging.info('Player ' + match[0].name + ' already loaded.')
            return match[0]



        if from_file:
            json = readjson_file('./data/races_' + name + '.txt')
        else:
            json = readjson('http://api.speedrunslive.com/pastraces?player=' + name + '&pageSize=1500')

        if json:
            logging.info('Loading player ' + name)
            player = Player(name, json, self)
            self.players.append(player)
            return player
        else:
            json = readjson('https://www.speedrun.com/api/v1/users?lookup=' + name)
            if json['data'] != []:
                new_name = json['data'][0]['names']['international']
                if new_name.lower() != name.lower():
                    return self.get_player(new_name)

        return Player('-1', None, None) # player not found