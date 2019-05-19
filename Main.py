from Dashboard.Dash import Dashboard
from SpeedRunsLive.SRL_data import SRL
import Logger
import logging



if __name__ == '__main__':

    srl = SRL()
    Logger.initalize_logger()


    dashboard = Dashboard(srl)
    dashboard.run_dashboard()