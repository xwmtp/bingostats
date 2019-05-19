import dash_core_components as dcc
import plotly.graph_objs as go

#### GRAPH 2 - SRL points ####

def get_SRL_point_graph(player, colors):
    races = player.select_races(sort='latest')

    dates          = [race.date   for race in races]
    points         = [race.points for race in races]

    markers        = [race.date.strftime('%b %d')+"<br>"+str(race.points) for race in races]


    graph = dcc.Graph(
            id='points',
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
                'layout': go.Layout(
                    title={'text': 'SRL point progression', 'font': {'color': colors['title']}},
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    font={
                        'color': colors['text']
                    },
                    height=600,
                    xaxis={'title': 'Date', 'gridcolor' : '#222222', 'linecolor':'#333333'},
                    yaxis={'title': 'Points', 'gridcolor' : '#222222', 'linecolor':'#333333'},
                    margin={'l': 75, 'b': 75, 't': 150, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )

    return graph