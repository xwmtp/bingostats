from Dashboard.Plots.Layout import colors
import dash_html_components as html
import dash_core_components as dcc


def get_html():
    return html.Div([

        html.Div([

            html.H1('OoT Bingo Stats'),
            html.Div('Enter Racetime/SRL user name:'),
            dcc.Input(id='input-field', value='', type='text', maxLength=50, spellCheck=False),
            html.Button('submit', id='button'),

            html.Div([
                dcc.Checklist(id='beta-checkbox',
                              options=[{
                                  'label': 'Include beta versions',
                                  'value': 'use_betas'
                              }],
                              value=['use_betas'],
                              labelStyle={'display': 'flex', 'alignItems': 'center', 'justify-content': 'center'}
                              ),
            ], id='beta-checkbox-div'),

        ]),

        html.Div(id='storage-div', children=[
            dcc.Loading([
                html.Div(id='storage-div-inner', children=[
                    dcc.Store(id='storage', storage_type='memory')
                ])
            ], color=colors['title'])
        ]),

        html.Div([
            html.Div([
                html.H2('', id='player-title'),
                html.Div(id='stats'),
                html.Div(id='ranks-graph', ),
            ], id='stats-ranks-graph'),

            html.Div([

                html.Div(id='srl-point-graph'),

                html.Div([
                    html.Div(html.Div(id='pb-graph-2'), id='pb-graph'),
                    html.Div([
                        html.Div('Show PBs for:', id='pb-dropdown-title'),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[],
                            clearable=False,
                            searchable=False,
                            placeholder='Version...'
                        )
                    ], id='pb-dropdown', className='no-display')
                ], id='pb-graph-div'),
            ], id='smaller-graphs'),

            html.Div(id='bingo-table'),

            # divs only used to store dash information, not displayed
            html.Div('', id='current-player', className='no-display'),
            html.Div('', id='use-betas', className='no-display'),
            html.Div('', id='current-version', className='no-display'),

        ], id='graphs', className='no-display'),

        html.A([
            html.Div('by xwillmarktheplace', id='footer-text'),
            html.Img(id='twitch-logo', src="/assets/TwitchGlitchWhite.png")
        ], id='footer', href="https://twitch.tv/xwillmarktheplace", target='_blank'),

    ], id='page')
