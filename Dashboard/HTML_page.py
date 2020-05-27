from Dashboard.Plots.Ranks_graph import get_ranks_graph
from Dashboard.Plots.SRL_point_graph import get_SRL_point_graph
from Dashboard.Plots.PB_graph import get_PB_graph
import dash_html_components as html
import dash_core_components as dcc

def get_html():

    return html.Div([

            html.Div([
                html.H1('OoT Bingo Stats'),
                html.Div('Enter SRL user name:'),
                dcc.Input(id='input-field', value='', type='text'),
                html.Button('submit', id='button')
            ]),
            html.H2('', id='player-title'),
            html.Div(id = 'stats'),

            dcc.Graph(id='ranks-graph', figure = get_ranks_graph()),

            html.Div([
                html.Div([
                    dcc.Graph(id='srl-point-graph', figure = get_SRL_point_graph()),
                ], id = 'srl-point-div'),

                html.Div([
                    dcc.Graph(id='pb-graph', figure = get_PB_graph()),
                    html.Div([
                        html.Div('Show PBs for:', id='pb-dropdown-title'),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[],
                            clearable=False,
                            searchable=False,
                            placeholder = 'Version...'
                        )
                    ], id='pb-dropdown')
                ], id='pb-graph-div'),

            ], id='smaller-graphs-div'),

            html.H3('Bingo races table'),
            html.Div(id = 'bingo-table'),
            html.Div('', id='current-player', className='no-display'),

            html.A([
                html.Div('by xwillmarktheplace', id='footer-text'),
                html.Img(id='twitch-logo', src="/assets/TwitchGlitchWhite.png")

            ], id='footer', href="https://twitch.tv/xwillmarktheplace", target='_blank')
        ], id='page')