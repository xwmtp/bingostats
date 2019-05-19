# -*- coding: utf-8 -*-
from Dashboard.Ranks_graph import get_ranks_graph
from Dashboard.SRL_point_graph import get_SRL_point_graph
from Dashboard.PB_graph import get_PB_graph
from Dashboard.Bingo_table import get_bingo_table
from Dashboard.Header_markdown import get_header_markdown
import dash

import dash_html_components as html


LABELS = {"Deep RBA" : "purple", "No ZL" : "red", "Child ZL" : "green", "Blank" : "grey"}


colors = {
    'background' : '#111111',
    'title' : '#e09456',
    'text' : '#bec7d2'
}



def run_dashboard(player):

    app = dash.Dash()


    graphs = [
        html.Div([
            get_header_markdown(player)
        ], style = {'textAlign' : 'center', 'color' : 'white'}),
        html.Div([
            get_ranks_graph(player, colors)
        ], style = {'width' : '80%', 'display': 'inline-block'}),
        html.Div([

            html.Div([
                get_SRL_point_graph(player, colors)
            ], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                get_PB_graph(player, colors)
            ], style={'width': '49%', 'display': 'inline-block'}),

        ]),
        html.Div([
            get_bingo_table(player, colors)
        ], style = {'width': '75%', 'display': 'inline-block', 'virtualization' : 'False', 'pagination_mode' : 'False', 'padding' : '100px'})

    ]

    style = {'font-family' : 'Calibri',
             'backgroundColor' : colors['background'],
             'textAlign' : 'center'
            }


    app.layout = html.Div(style=style, children = graphs)

    app.run_server(debug=True)
    print('running!!!!')


def get_intro_markdown_text(player, name):
    # overall stats
    all_races = player.select_races(type="bingo", forfeits=True)
    compl_races = player.select_races(type="bingo", forfeits=False)
    num_blanks = len([r for r in compl_races if r.row_id == 'BLANK'])
    num_races = len(compl_races)
    num_forfeits = len([r for r in all_races if r.forfeit])
    num_all_races = len(all_races)

    forfeits = [r for r in compl_races if r.row_id == 'BLANK']
    #for f in forfeits:
    #    f.print_race(row=False)

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



