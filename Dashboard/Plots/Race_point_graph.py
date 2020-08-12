from Dashboard.Plots.Layout import get_graph_layout
import dash_core_components as dcc
import plotly.graph_objs as go

def get_race_point_graph(player=None):
    graph = []

    if player:
        races = player.select_races(sort='latest')


        srl_races = [race for race in races if race.platform == 'srl']
        rt_races = [race for race in races if race.platform == 'racetime']

        if len(rt_races) > 20 or len(rt_races) > len(srl_races):
            races = rt_races
            platform = 'Racetime'
        else:
            races = srl_races
            platform = 'SRL'

        dates = [race.date for race in races]
        points = [race.points for race in races]
        markers = [race.date.strftime('%b %d') + "<br>" + str(race.points) for race in races]

        data = [go.Scatter(
            x=dates,
            y=points,
            mode='lines+markers',
            text=markers,
            marker={
                'size': 7,
                'line': {'width': 0.5, 'color': 'black'},
                'color': 'lightblue'
            },
            line=dict(
                shape='vh'
            ),
            hoverinfo='text'
        )]

        graph = [dcc.Graph(
                      figure={'data': data,
                              'layout': get_graph_layout(title=f'{platform} points progression', height=600, y_label='Points', tickformat='')
                              }
                      )]

    return graph