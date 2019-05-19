import dash_core_components as dcc
import plotly.graph_objs as go
import Utils

#### GRAPH 1 - Ranks ####

def get_ranks_graph(player, colors):
    races = player.select_races()
    points = [Data_point(race) for race in races]

    dates          = [point.date          for point in points]
    times          = [point.scatter_time  for point in points]
    relative_ranks = [point.relative_rank for point in points]
    markers        = [point.marker        for point in points]


    graph = dcc.Graph(
        id='bingo-scatter-ranks',
        figure={
            'data': [
                go.Scatter(
                    x=dates,
                    y=times,
                    text=markers,
                    mode='markers',
                    opacity=1,
                    marker={
                        'size': 12,
                        'line': {'width': 0.5, 'color': 'black'},
                        'color': relative_ranks,
                        'showscale':True
                    },
                    hoverinfo='text'
                )
            ],
            'layout': go.Layout(
                title={'text': 'Bingo results', 'font': {'color': colors['title']}},
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font={
                    'color': colors['text']
                },
                xaxis={'title': 'Date', 'gridcolor' : '#222222', 'linecolor':'#333333'},
                yaxis={'title': 'Time', 'gridcolor' : '#222222', 'linecolor':'#333333', 'tickformat': '%H:%M:%S'},
                height = 650,
                margin={'l': 75, 'b': 75, 't': 150, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )

    return graph



class Data_point:

    def __init__(self, race):
        self.date = race.date
        self.relative_rank = self.relative_rank(race)
        time = race.time.total_seconds()
        self.scatter_time, human_time = Utils.convert_to_human_readable_time(time)

        self.marker = self.date.strftime('%b %d') + '<br>' + race.type + '<br>'+str(human_time)+'<br>rank: '+str(race.rank)+'/'+str(race.total_players)

    def relative_rank(self, race):
        return (1 / (race.total_players - 1)) * (race.rank - 1)