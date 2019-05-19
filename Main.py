from Dashboard.Dash import run_dashboard
from SpeedRunsLive.SRL_data import SRL
import Logger
import logging



if __name__ == '__main__':

    srl = SRL()
    Logger.initalize_logger()

    name = 'xwillmarktheplace'

    player = srl.get_player(name)
    if player:
        run_dashboard(player)
    else:
        logging.info('Player ' + name + ' not found!')