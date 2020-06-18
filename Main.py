from Dashboard.Dash import Dashboard
import Logger
import logging
import sys


# python main.py host debug log_level
if __name__ == '__main__':

    try:
        log_level = int(sys.argv[3])
    except IndexError:
        log_level = logging.INFO

    Logger.initalize_logger(log_level)
    logging.info('Starting BingoStats...')

    try:
        host = sys.argv[1]
    except IndexError:
        host = '127.0.0.1'

    try:
        debug = sys.argv[2] == 'True'
    except IndexError:
        debug = True

    dashboard = Dashboard()
    dashboard.run_dashboard(host, debug)