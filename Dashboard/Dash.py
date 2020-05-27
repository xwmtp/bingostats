# -*- coding: utf-8 -*-
from Dashboard.Plots.Ranks_graph import get_ranks_graph
from Dashboard.Plots.SRL_point_graph import get_SRL_point_graph
from Dashboard.Plots.PB_graph import get_PB_graph, get_dropdown_options
from Dashboard.Plots.Bingo_table import get_bingo_table
from Dashboard.Stats_text import get_stats_divs
from Dashboard.HTML_page import get_html
import dash
from dash.dependencies import Input, Output, State
import logging


class Dashboard:

    def __init__(self, srl):
        self.srl = srl


    def run_dashboard(self, host, debug=False):

        logging.info('Starting up Dash app...')
        app = dash.Dash()
        app.title = 'OoT Bingo Stats'
        app.layout = get_html()

        self.setup_app_callbacks(app)
        app.run_server(debug=debug, host=host, port=80)


    def setup_app_callbacks(self, app):

        # Upon changing the current player
        @app.callback([
            Output(component_id='stats', component_property='children'),
            Output(component_id='ranks-graph', component_property='figure'),
            Output(component_id='srl-point-graph', component_property='figure'),
            Output(component_id='bingo-table', component_property='children'),
            Output(component_id='dropdown', component_property='value'),
            Output(component_id='dropdown', component_property='options'),
            Output(component_id='player-title', component_property='children'),
        ],
            [Input(component_id='current-player', component_property='children')]
        )
        def update_output_div(input_value):
            player = self.srl.get_player(input_value)
            markdown = get_stats_divs(player, input_value)
            ranks_graph = get_ranks_graph(player)
            srl_point_graph = get_SRL_point_graph(player)
            bingo_table = get_bingo_table(player) if player else []
            current_version = player.get_latest_version() if player else 'all'
            versions_options = get_dropdown_options(player)
            player_name = player.name if player else ''
            logging.info(f"Loaded player '{player_name}'")
            return markdown, ranks_graph, srl_point_graph, bingo_table, current_version, versions_options, player_name


        # Upon entering a different name in the field
        @app.callback(
            Output(component_id='current-player', component_property='children'),
            [Input(component_id='input-field', component_property='n_submit'),
             Input(component_id='button', component_property='n_clicks')],
            [State(component_id='input-field', component_property='value')]
        )
        def update_current_player(n_submit, n_clicks, input_value):
            try:
                logging.info(f"Submitted: '{input_value}'")
                return input_value
            except UnicodeEncodeError as e:
                print('error!!!!!!!!!!')
                logging.info(e)
                return ''


        # Upon changing the bingo version in the dropdown
        @app.callback(
            Output('pb-graph', 'figure'),
            [Input('dropdown', 'value')],
            [State('current-player', 'children')]
        )
        def update_version(version, player_title):
            player = self.srl.get_player(player_title)
            PB_graph = get_PB_graph(player, version)
            if player:
                logging.info(f"Loaded {version} PB graph for player '{player_title}'")
            return PB_graph