from Dashboard.Dash import Dashboard
from SpeedRunsLive.SRL_data import SRL
import Logger
import logging
import sys



if __name__ == '__main__':

    try:
        log_level = sys.argv[3]
    except IndexError:
        log_level = logging.INFO

    Logger.initalize_logger(log_level)
    logging.info('Starting BingoStats...')

    srl = SRL()

    try:
        host = sys.argv[1]
    except IndexError:
        host = '127.0.0.1'

    try:
        debug = sys.argv[2]
    except IndexError:
        debug = True

    dashboard = Dashboard(srl)
    dashboard.run_dashboard(host, debug)