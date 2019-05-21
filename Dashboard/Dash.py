# -*- coding: utf-8 -*-
from Dashboard.Ranks_graph import get_ranks_graph
from Dashboard.SRL_point_graph import get_SRL_point_graph
from Dashboard.PB_graph import get_PB_graph, get_dropdown_options
from Dashboard.Bingo_table import get_bingo_table
from Dashboard.Stats_text import get_stats_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import logging
import base64




class Dashboard:

    def __init__(self, srl):

        self.srl = srl
        self.colors = {
            'background' : '#111111',
            'title' : '#e09456',
            'text' : '#bec7d2'
        }
        self.current_player = srl.get_player('')



    def run_dashboard(self):

        app = dash.Dash()
        app.title = 'OoT Bingo Stats'

        components = [
            html.Div([
                html.Div('By:', style={'color': 'white', 'textAlign' : 'center'}),
                html.A(html.Img(src=app.get_asset_url('Logo.png')), href = 'https://www.twitch.tv/xwillmarktheplace'),
            ], style = {'left' : 0, 'position' : 'absolute', 'margin-top' : '1px', 'display': 'inline-block'}),
            html.Div([
                html.H1('OoT Bingo Stats', style={'textAlign': 'center', 'color': 'white', 'fontSize': '65px'}),
                html.Div('Enter SRL user name:', style={'color': 'white'}),
                dcc.Input(id='input-field', value='', type='text')
            ], style = {'float' : 'center', 'display': 'inline-block' }),
            html.Div(
                id = 'stats', style = {'textAlign' : 'center', 'color' : 'white'}),

            html.Div([
                dcc.Graph(id='ranks-graph', figure = {'layout' : self.graph_layout('Bingo races', 650, self.colors)})
            ], style = {'width' : '80%', 'display': 'inline-block'}),
            html.Div([

                html.Div([
                    dcc.Graph(id='srl-point-graph', figure = {'layout' : self.graph_layout('SRL points progression', 600, self.colors)})
                ], style={'width': '49%', 'height' : '655px', 'display': 'inline-block'}),

                html.Div([
                    dcc.Graph(id='PB-graph', figure = {'layout' : self.graph_layout('PB progression', 600, self.colors)}),
                    html.Div([
                        html.Div('Show PBs for:', style={'color': 'white', 'float': 'right'}),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[],
                            clearable=False,
                            placeholder = 'Version...',
                            style = {'width' : 90, 'float': 'right'}
                        )
                    ], style = {'width' : 150, 'textAlign' : 'left', 'float': 'right', 'display': 'inline-block'})
                ], style={'width': '49%','display': 'inline-block', 'alignItems' : 'right'}),

            ]),
            html.Div('Bingo races table', style = {'textAlign' : 'center', 'color' : self.colors['title'], 'fontSize' : '20px', 'padding-top' : '45px'}),
            html.Div(
            id = 'bingo-table', style = {'width': '72%', 'display': 'inline-block', 'virtualization' : 'True', 'pagination_mode' : 'False', 'padding' : '30px'})

        ]

        style = {'font-family' : 'Calibri',
                 'backgroundColor' : self.colors['background'],
                 'textAlign' : 'center'
                }

        app.layout = html.Div(style=style, children = components)

        @app.callback(
            Output('PB-graph', 'figure'),
            [Input('dropdown', 'value')]
        )
        def update_version(version):
            return get_PB_graph(self.current_player, self.graph_layout('PB progression', 600, self.colors), version)

        @app.callback([
             Output(component_id='stats', component_property='children'),
             Output(component_id='ranks-graph',     component_property='figure'),
             Output(component_id='srl-point-graph', component_property='figure'),
             Output(component_id='dropdown',        component_property='value'),
             Output(component_id='bingo-table', component_property='children'),
             Output(component_id='dropdown',    component_property='options')
            ],
            [Input(component_id='input-field', component_property='n_submit')],
            [State(component_id='input-field', component_property='value')]
        )
        def update_output_div(n_submit, input_value):
            player = self.srl.get_player(input_value)
            self.current_player = player
            markdown         = get_stats_text      (player, input_value)
            ranks_graph      = get_ranks_graph     (player, self.graph_layout('Bingo races', 650, self.colors))
            srl_point_graph  = get_SRL_point_graph (player, self.graph_layout('SRL points progression', 600, self.colors, y_label='Points', tickformat=''))
            PB_graph         = player.get_latest_version()
            bingo_table      = get_bingo_table     (player, self.colors)
            versions_options = get_dropdown_options(player)
            logging.info('Loading complete.')
            return markdown, ranks_graph, srl_point_graph, PB_graph, bingo_table, versions_options

        app.run_server(debug=True)


    def graph_layout(self, title, height, colors, y_label='Time', tickformat='%-Hh%M'):
        return go.Layout(
            title={'text': title, 'font': {'color': colors['title']}},
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font={
                'color': colors['text']
            },
            height=height,
            xaxis={'title': 'Date', 'gridcolor': '#222222', 'linecolor': '#333333'},
            yaxis={'title': y_label, 'gridcolor': '#222222', 'linecolor': '#333333', 'tickformat': tickformat},
            margin={'l': 75, 'b': 50, 't': 150, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )


