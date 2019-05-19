# -*- coding: utf-8 -*-
from Dashboard.Ranks_graph import get_ranks_graph
from Dashboard.SRL_point_graph import get_SRL_point_graph
from Dashboard.PB_graph import get_PB_graph
from Dashboard.Bingo_table import get_bingo_table
from Dashboard.Header_markdown import get_header_markdown
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging




class Dashboard:

    def __init__(self, srl):

        self.srl = srl
        self.colors = {
            'background' : '#111111',
            'title' : '#e09456',
            'text' : '#bec7d2'
        }

        self.players = []



    def run_dashboard(self):

        app = dash.Dash()

        #player = self.srl.get_player('scaramanga')

        graphs = [
            #html.Div([
            #    get_header_markdown()
            #], style = {'textAlign' : 'center', 'color' : 'white'}),
            html.Div([
                dcc.Input(id='my-id', value='xwillmarktheplace', type='text'),
                html.Div(id='my-div', style={'color' : 'white'})
            ]),
            html.Div([
                dcc.Graph(id='ranks-graph')
            ], style = {'width' : '80%', 'display': 'inline-block'}),
            html.Div([

                html.Div([
                    dcc.Graph(id='srl-point-graph')
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Graph(id='PB-graph')
                ], style={'width': '49%', 'display': 'inline-block'}),

            ]),
            html.Div(
            id = 'bingo-table', style = {'width': '75%', 'display': 'inline-block', 'virtualization' : 'True', 'pagination_mode' : 'False', 'padding' : '100px'})

        ]

        style = {'font-family' : 'Calibri',
                 'backgroundColor' : self.colors['background'],
                 'textAlign' : 'center'
                }

        app.layout = html.Div(style=style, children = graphs)

        @app.callback([
             Output(component_id='my-div', component_property='children'),
             Output(component_id='ranks-graph',     component_property='figure'),
             Output(component_id='srl-point-graph', component_property='figure'),
             Output(component_id='PB-graph',        component_property='figure'),
             Output(component_id='bingo-table', component_property='children')
            ],
            [Input(component_id='my-id', component_property='n_submit')],
            [State(component_id='my-id', component_property='value')]
        )
        def update_output_div(n_submit, input_value):
            player = self.get_player(input_value)
            logging.info('Found player ' + player.name)
            input_text = "Loaded player '{}'.".format(input_value)
            ranks_graph     = get_ranks_graph(player, self.colors)
            srl_point_graph = get_SRL_point_graph(player, self.colors)
            PB_graph        = get_PB_graph(player, self.colors)
            bingo_table     = get_bingo_table(player, self.colors)
            return input_text, ranks_graph, srl_point_graph, PB_graph, bingo_table



        app.run_server(debug=True)


    def get_player(self, name):
        match = [player for player in self.players if name.lower() == player.name]
        if len(match) > 0:
            return match[0]
        else:
            player = self.srl.get_player(name)
            self.players.append(player)
            return player


def get_intro_markdown_text(player, name):
    # overall stats
    all_races = player.select_races(type="bingo", forfeits=True)
    compl_races = player.select_races(type="bingo", forfeits=False)
    num_blanks = len([r for r in compl_races if r.row_id == 'BLANK'])
    num_races = len(compl_races)
    num_forfeits = len([r for r in all_races if r.forfeit])
    num_all_races = len(all_races)

    blank_perc = round((num_blanks / num_races) * 100, 1)
    forfeit_perc = round((num_forfeits / num_all_races) * 100, 1)

    bf_name = name
    name_len = len(bf_name)

    if blank_perc > 30:
        bf_name = bf_name[0:(int(name_len / 2)) + 1] + " 'blank' "  + bf_name[(int(name_len / 2)) + 1:name_len]
    elif forfeit_perc > 50:
        bf_name = bf_name[0:(int(name_len / 2)) + 1] + " 'forfeit' " + bf_name[(int(name_len / 2)) + 1:name_len]

    markdown_text = '# Bingo Stats {}\n\nCompleted {} bingo races since v9.2.\n\nBlanked {} completed races ({})%.\n\nForfeited {} races ({})%.\n\n'.format(bf_name, num_races, num_blanks, blank_perc, num_forfeits, forfeit_perc)

    return markdown_text



