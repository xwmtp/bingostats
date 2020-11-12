# -*- coding: utf-8 -*-
from Dashboard.Plots.Ranks_graph import get_ranks_graph
from Dashboard.Plots.Race_point_graph import get_race_point_graph
from Dashboard.Plots.PB_graph import get_PB_graph, get_dropdown_options
from Dashboard.Plots.Bingo_table import get_bingo_table
from Dashboard.Stats_text import get_stats_divs
from Dashboard.HTML_page import get_html
from RaceData.RaceData import get_player, load_player_data
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import logging


class Dashboard:

    def run_dashboard(self, host, debug=False):

        logging.info('Starting up Dash app...')
        app = dash.Dash()
        app.title = 'OoT Bingo Stats'
        app.layout = get_html()

        self.setup_app_callbacks(app)
        app.run_server(debug=debug, host=host, port=80)

    def setup_app_callbacks(self, app):

        @app.callback(Output('storage', 'data'),
                      [Input(component_id='current-player', component_property='children'),
                       Input(component_id='use-betas', component_property='children'),
                       ],
                      [State('storage', 'data')])
        def update_player_data(input_name, include_betas, current_data):
            if input_name is '':
                # prevent the None callbacks is important with the store component.
                # you don't want to update the store for nothing.
                logging.debug('PreventUpdate for update_player_data()')
                raise PreventUpdate

            if current_data and current_data['name'] == input_name:
                player_data = current_data
            else:
                player_data = load_player_data(input_name, include_betas) or {}
            return player_data


        @app.callback([
            Output(component_id='stats', component_property='children'),
            Output(component_id='ranks-graph', component_property='children'),
            Output(component_id='srl-point-graph', component_property='children'),
            Output(component_id='bingo-table', component_property='children'),
            Output(component_id='pb-graph', component_property='children'),
            Output(component_id='pb-dropdown', component_property='className'),
            Output(component_id='dropdown', component_property='value'),
            Output(component_id='dropdown', component_property='options'),
            Output(component_id='player-title', component_property='children'),
        ],
            [Input('storage', 'modified_timestamp')],
            [State('storage', 'data')]
        )
        def update_output_div(ts, data):
            if ts is None or data is None:
                logging.debug('PreventUpdate for update_output_div()')
                raise PreventUpdate

            player = get_player(data)
            markdown = get_stats_divs(player, player.name)
            ranks_graph = get_ranks_graph(player)
            srl_point_graph = get_race_point_graph(player)
            bingo_table = get_bingo_table(player) if player else []
            current_version = player.get_latest_version() if player else ''
            versions_options = get_dropdown_options(player)
            PB_graph = get_PB_graph(player, current_version, True)
            dropdown_visibility = 'display' if player else 'no-display'
            player_name = player.name if player else ''
            if player and player.name:
                logging.info(f"Loaded data of user '{player_name}'")
            return markdown, ranks_graph, srl_point_graph, bingo_table, PB_graph, dropdown_visibility, current_version, versions_options, player_name

        # Called upon entering a different name in the field
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
            display = 'no-display'
            if input_value:
                logging.info(f"Submitted user name '{input_value}'")
                display = 'display'
            return input_value, display

        # Called upon checking/unchecking beta-version checkbox
        @app.callback(
            Output('use-betas', 'children'),
            [Input('beta-checkbox', 'value')],
            [State('use-betas', 'children')]
        )
        def update_version(beta_values, current_value):
            beta_value = len(beta_values) > 0  # when checkbox is checked, use_betas list is non-empty
            value_was_changed = current_value != '' and beta_value != current_value
            if value_was_changed:
                logging.info(f"Set 'use betas' to '{beta_value}'")
            return beta_value

        # Called upon changing the bingo version in the dropdown
        @app.callback(
            [Output('pb-graph-2', 'children'),
             Output('current-version', 'children')],
            [Input('dropdown', 'value')],
            [State('current-version', 'children'),
             State('storage', 'data')
             ]
        )
        def update_pb_version(new_version, current_version, data):
            player = get_player(data)
            PB_graph = get_PB_graph(player, new_version)
            value_was_changed = current_version != '' and new_version != current_version
            if player and value_was_changed:
                logging.info(f"Set PB graph version to '{new_version}'")
            return PB_graph, new_version
