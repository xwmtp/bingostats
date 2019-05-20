import dash_core_components as dcc
import plotly.graph_objs as go

#### GRAPH 2 - SRL points ####

def get_SRL_point_graph(player, layout):
    races = player.select_races(sort='latest')

    dates          = [race.date   for race in races]
    points         = [race.points for race in races]

    markers        = [race.date.strftime('%b %d')+"<br>"+str(race.points) for race in races]



    figure={
        'data': [
            go.Scatter(
                x=dates,
                y=points,
                mode='lines+markers',
                text = markers,
                marker={
                    'size': 7,
                    'line': {'width': 0.5, 'color': 'black'},
                    'color': 'lightblue'
                },
                line = dict(
                    shape = 'vh'
                ),
                hoverinfo='text'

            )
        ],
        'layout': layout
    }

    return figure