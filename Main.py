from Dashboard.Dash import Dashboard
from SpeedRunsLive.SRL_data import SRL
import Logger
import logging



if __name__ == '__main__':

    Logger.initalize_logger()
    logging.info('Starting BingoStats...')

    srl = SRL()

    dashboard = Dashboard(srl)
    dashboard.run_dashboard()