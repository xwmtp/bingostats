# -*- coding: utf-8 -*-
from Dashboard.Ranks_graph import get_ranks_graph
from Dashboard.SRL_point_graph import get_SRL_point_graph
from Dashboard.PB_graph import get_PB_graph
from Dashboard.Bingo_table import get_bingo_table
from Dashboard.Stats_text import get_stats_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
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



    def run_dashboard(self):

        app = dash.Dash()
        app.title = 'OoT Bingo Stats'



        components = [
            html.H1('OoT Bingo Stats', style = {'textAlign' : 'center', 'color' : 'white', 'fontSize' : '65px'}),
            html.Div([
                html.Div('Enter SRL user name:', style={'color': 'white'}),
                dcc.Input(id='input-field', value='', type='text')
            ]),
            html.Div(
                id = 'stats', style = {'textAlign' : 'center', 'color' : 'white'}),

            html.Div([
                dcc.Graph(id='ranks-graph', figure = {'layout' : self.graph_layout('Bingo races', 650, self.colors)})
            ], style = {'width' : '80%', 'display': 'inline-block'}),
            html.Div([

                html.Div([
                    dcc.Graph(id='srl-point-graph', figure = {'layout' : self.graph_layout('Bingo races', 600, self.colors)})
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Graph(id='PB-graph', figure = {'layout' : self.graph_layout('Bingo races', 600, self.colors)})
                ], style={'width': '49%', 'display': 'inline-block'}),

            ]),
            html.Div('Bingo races table', style = {'textAlign' : 'center', 'color' : self.colors['title'], 'fontSize' : '20px'}),
            html.Div(
            id = 'bingo-table', style = {'width': '75%', 'display': 'inline-block', 'virtualization' : 'True', 'pagination_mode' : 'False', 'padding' : '30px'})

        ]

        style = {'font-family' : 'Calibri',
                 'backgroundColor' : self.colors['background'],
                 'textAlign' : 'center'
                }

        app.layout = html.Div(style=style, children = components)

        @app.callback([
             Output(component_id='stats', component_property='children'),
             Output(component_id='ranks-graph',     component_property='figure'),
             Output(component_id='srl-point-graph', component_property='figure'),
             Output(component_id='PB-graph',        component_property='figure'),
             Output(component_id='bingo-table', component_property='children')
            ],
            [Input(component_id='input-field', component_property='n_submit')],
            [State(component_id='input-field', component_property='value')]
        )
        def update_output_div(n_submit, input_value):
            player = self.srl.get_player(input_value)
            markdown        = get_stats_text     (player, input_value)
            ranks_graph     = get_ranks_graph    (player, self.graph_layout('Bingo races', 650, self.colors))
            srl_point_graph = get_SRL_point_graph(player, self.graph_layout('SRL points progression', 600, self.colors, y_label='Points', tickformat=''))
            PB_graph        = get_PB_graph       (player, self.graph_layout('PB progression', 600, self.colors))
            bingo_table     = get_bingo_table    (player, self.colors)
            logging.info('Loading complete.')
            return markdown, ranks_graph, srl_point_graph, PB_graph, bingo_table

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
            margin={'l': 75, 'b': 75, 't': 150, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )


