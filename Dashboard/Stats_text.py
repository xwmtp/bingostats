from Definitions import is_supported_version
import dash_core_components as dcc
import dash_html_components as html
import logging

def get_stats_divs(player, input):

    divs = []

    if player:
        general_stats_text = _get_general_stats_string(player)
        row_stats_text = _get_rows_stats_string(player)
        divs = [html.Div(dcc.Markdown(general_stats_text), className = 'stats-block'),
                     html.Div(dcc.Markdown(row_stats_text), className = 'stats-block')]
    elif input:
        divs = [html.Div(f"User '{input}' not found.", className = 'user-not-found')] # a non-empty name was submitted
        logging.info(f"Submitted user name '{input}' was not found")

    return divs


def _get_general_stats_string(player):
    all_races = player.select_races(type="bingo", forfeits=True)
    completed_races = player.select_races(type="bingo", forfeits=False)

    blank_races = [r for r in completed_races if
                   r.type != 'v2' and r.type != 'v3']  # posting rows was not really a thing in v2/3
    num_blanks = len([r for r in blank_races if r.row_id == 'blank'])
    num_forfeits = len([r for r in all_races if r.forfeit])

    blank_perc = perc(num_blanks, len(blank_races))
    forfeit_perc = perc(num_forfeits, len(all_races))

    logging.debug('{} bingos, {} excl forfeits, {} bingos without v2/v3, {} of which were blanked.'.format(
        len(all_races), len(completed_races), len(blank_races), num_blanks
    ))

    blank_shame = ' .shame' if blank_perc > 25 else ''
    forfeit_shame = ' .shame' if forfeit_perc > 25 else ''

    return f'Completed {len(completed_races)} bingos\n\n' \
           f'Blanked {num_blanks} bingos ({blank_perc}%){blank_shame}\n\n' \
           f'Forfeited {num_forfeits} bingos ({forfeit_perc}%){forfeit_shame}\n\n'

def _get_rows_stats_string(player):
    completed_races = player.select_races(type="bingo", forfeits=False)
    favorite_row = player.get_favorite_row()
    rows_text = f'Most common row: {favorite_row}\n\n'

    versions = list(set([race.type for race in completed_races]))
    versions = sorted(versions)
    for version in versions:
        version_races = [race for race in completed_races if race.type == version]
        if is_supported_version(version):
            favorite_goal = player.get_favorite_goal(version)
            if favorite_goal:
                fav_goal = player.short_goal_dict[favorite_goal]
                count = len([race for race in version_races if favorite_goal in race.row])
                fav_goal_perc = perc(count, len(version_races), 1)
                rows_text = rows_text + f'Most common goal in {version}: {fav_goal} ({fav_goal_perc}%)\n\n'
    return rows_text


def perc(small, big, decimals=1):
    return round((small / big) * 100, decimals) if big > 0 else 0

