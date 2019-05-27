from Definitions import is_supported_version
import dash_core_components as dcc
import dash_html_components as html
import logging

def get_stats_text(player, input):

    def perc(small, big, decimals=1):
        return round((small / big) * 100, decimals) if big > 0 else 0

    # overall stats
    all_races = player.select_races(type="bingo", forfeits=True)
    completed_races = player.select_races(type="bingo", forfeits=False)
    blank_races = [r for r in completed_races if r.type != 'v2' and r.type != 'v3'] #posting rows was not really a thing in v2/3
    num_blanks = len([r for r in blank_races if r.row_id == 'blank'])
    num_forfeits = len([r for r in all_races if r.forfeit])


    blank_perc   = perc(num_blanks, len(blank_races))
    forfeit_perc = perc(num_forfeits, len(all_races))

    logging.debug('{} bingos, {} excl forfeits, {} bingos without v2/v3, {} of which were blanked.'.format(
        len(all_races), len(completed_races), len(blank_races), num_blanks
    ))

    blank_shame   = ' .shame' if blank_perc   > 25 else ''
    forfeit_shame = ' .shame' if forfeit_perc > 25 else ''


    if player.name == '-1':
        text = "User '" + input + "' not found."
    elif player.name == '':
        text = ''
    else:
        text = 'Completed {} bingos.\n\n' \
               'Blanked {} bingos ({}%){}\n\n' \
               'Forfeited {} bingos ({}%){}\n\n'\
               .format(len(completed_races),
                       num_blanks, blank_perc, blank_shame,
                       num_forfeits, forfeit_perc, forfeit_shame
               )

    rows_text = ''
    favorite_row  = player.get_favorite_row()
    if favorite_row:
        rows_text = rows_text + 'Most common row: ' + favorite_row + '\n\n'

    versions = list(set([race.type for race in completed_races]))
    versions = sorted(versions)
    for version in versions:
        version_races = [race for race in completed_races if race.type == version]
        if is_supported_version(version):
            favorite_goal = player.get_favorite_goal(version)
            if favorite_goal:
                count = len([race for race in version_races if favorite_goal in race.row])
                rows_text = rows_text + 'Most common goal in {}: {} ({}%)\n\n'.format(version, player.short_goal_dict[favorite_goal], perc(count,len(version_races),1))

    style = {'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}
    return html.Div([html.Div(dcc.Markdown(text),      style=style),
                     html.Div(dcc.Markdown(rows_text), style=style)])





