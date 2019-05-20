import plotly.graph_objs as go
import Utils
import datetime as dt
import logging
from Definitions import get_newest_version

#### GRAPH 1 - Ranks ####


def get_PB_graph(player, layout, version):
    races = player.select_races(sort='latest', type = version)

    if len(races) == 0:
        dates = []
        times = []
        markers = []
    else:

        PBs = get_PB_races(races)
        newest = get_newest_version()

        dates = [PB.date                 for PB in PBs]
        times = [PB.time.total_seconds() for PB in PBs]
        if version == newest:
            dates.append(dt.date.today()) # pb still valid today
            times.append(times[-1])  # need last elements twice

        markers = get_markers(times, dates, version, newest)
        times = [Utils.convert_to_human_readable_time(time)[0] for time in times]

    figure={
        'data': [
            go.Scatter(
                x=dates,
                y=times,
                mode='lines+markers',
                text=markers,
                marker={
                    'size': 9,
                    'line': {'width': 0.5, 'color': 'black'},
                    'color':'lightgreen'
                },
                line=dict(
                    shape='hv'
                ),
                hoverinfo='text'

            )
        ],
        'layout': layout
    }

    return figure



def get_PB_races(races):
    if len(races) < 1:
        return []

    races = races[::-1] # reverse the latest races to look from first to last

    best_race = races[0]
    PBs = [best_race]

    for race in races:
        if race.time < best_race.time:
            best_race = race
            PBs.append(best_race)

    return PBs

def get_dropdown_options(player):
        versions = player.get_versions()
        options = [{'label' :  'all', 'value' : 'bingo'}] + [{'label': version, 'value': version} for version in versions]
        return options




def get_markers(times, dates, version, newest):
    human_times = [Utils.convert_to_human_readable_time(time)[1] for time in times]

    diff_times = [abs(j - i) for i, j in zip(times[:-1], times[1:])]

    human_diff_times = [Utils.convert_to_human_readable_time(diff_time)[1] for diff_time in diff_times]

    diff_times = [''] + human_diff_times
    if version == newest:
        diff_times[-1] = ''

    markers = [d.strftime('%b %d') + '<br>' + str(t) + '<br>-' + str(f) for d, t, f in
               zip(dates, human_times, diff_times)]
    markers[0] = markers[0].replace('<br>-', '<br>First ' + version + ' race')  # different marker for first 'pb' time
    if version == newest:
        markers[-1] = markers[-1].replace('<br>-', '<br>Current ' + version + ' PB')  # different marker for first 'pb' time

    return markers
