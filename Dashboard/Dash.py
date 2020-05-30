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
            Output(component_id='ranks-graph', component_property='children'),
            Output(component_id='srl-point-graph', component_property='children'),
            Output(component_id='bingo-table', component_property='children'),
            Output(component_id='dropdown', component_property='value'),
            Output(component_id='dropdown', component_property='options'),
            Output(component_id='player-title', component_property='children'),
        ],
            [Input(component_id='current-player', component_property='children'),
             Input(component_id='use-betas', component_property='children'),
             ],
        )
        def update_output_div(input_name, include_betas):
            player = self.srl.get_player(input_name, include_betas)
            markdown = get_stats_divs(player, input_name)
            ranks_graph = get_ranks_graph(player)
            srl_point_graph = get_SRL_point_graph(player)
            bingo_table = get_bingo_table(player) if player else []
            current_version = player.get_latest_version() if player else ''
            versions_options = get_dropdown_options(player)
            player_name = player.name if player else ''
            if player and player.name:
                logging.info(f"Loaded player '{player_name}'")
            return markdown, ranks_graph, srl_point_graph, bingo_table, current_version, versions_options, player_name


        # Upon entering a different name in the field
        @app.callback(
            [Output(component_id='current-player', component_property='children'),
             Output(component_id='graphs', component_property='className')
             ]
             ,
            [Input(component_id='input-field', component_property='n_submit'),
             Input(component_id='button', component_property='n_clicks')],
            [State(component_id='input-field', component_property='value')]
        )
        def update_current_player(n_submit, n_clicks, input_value):
            display_graphs = 'no-display'
            if input_value:
                logging.info(f"Submitted user name '{input_value}'")
                display_graphs = 'display'
            return input_value, display_graphs


        # Upon checking/unchecking beta-version checkbox
        @app.callback(
            Output('use-betas', 'children'),
            [Input('beta-checkbox', 'value')],
            [State('use-betas', 'children')]
        )
        def update_version(beta_values, current_value):
            beta_value = len(beta_values) > 0 # when checkbox is checked, use_betas list is non-empty
            value_was_changed = current_value != '' and beta_value != current_value
            if value_was_changed:
                logging.info(f"Set 'use betas' to '{beta_value}'")
            return beta_value


        # Upon changing the bingo version in the dropdown
        @app.callback(
            [Output('pb-graph', 'children'),
            Output('current-version', 'children')],
            [Input('dropdown', 'value')],
            [State('current-player', 'children'),
             State('current-version', 'children'),
             ]
        )
        def update_pb_version(new_version, player_title, current_version):
            player = self.srl.get_player(player_title)
            PB_graph = get_PB_graph(player, new_version)
            value_was_changed = current_version != '' and new_version != current_version
            if player and value_was_changed:
                logging.info(f"Set PB graph version to '{new_version}'")
            return PB_graph, new_version
