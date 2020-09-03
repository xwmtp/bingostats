from Definitions import is_supported_version
from RaceData.Player import SHORT_GOAL_NAMES
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

    logging.debug(f'{len(all_races)} bingos, {len(completed_races)} excl forfeits, {len(blank_races)} bingos without v2/v3, {num_blanks} of which were blanked.')

    blank_shame = ' .shame' if blank_perc > 25 else ''
    forfeit_shame = ' .shame' if forfeit_perc > 25 else ''

    N = 10
    average, avg_forfeits = player.get_average(N)
    average_str = str(average).split('.')[0]
    median, med_forfeits = player.get_median(N)
    median_str = str(median).split('.')[0]
    forfeits_str = 'forfeit' if med_forfeits == 1 else 'forfeits'
    eff_median = player.get_effective_median(N)
    eff_median_str = str(eff_median).split('.')[0]

    return f'Completed {len(completed_races)} bingos\n\n' \
           f'Blanked {num_blanks} bingos ({blank_perc}%){blank_shame}\n\n' \
           f'Forfeited {num_forfeits} bingos ({forfeit_perc}%){forfeit_shame}\n\n' \
           f'Average over last {N} completed bingos: {average_str}\n\n' \
           f'Median over last {N} completed bingos: {median_str}\n\n' \
           f'Effective median over last {N} bingos: {eff_median_str} (incl {med_forfeits} {forfeits_str})'

def _get_rows_stats_string(player):
    if len(player.select_races(type="bingo")) == 0:
        return ''
    favorite_row, fav_row_count, fav_row_total = player.get_favorite_row()

    rows_text = f'Most common row: {favorite_row} ({round(fav_row_count/fav_row_total*100,1)}%)\n\n'

    versions = player.get_supported_versions(shorten_betas=True)
    for version in versions + ['bingo']:
        if is_supported_version(version):
            version_races = player.select_races(type=version, blanks=False)
            favorite_goal = player.get_favorite_goal(version)
            if favorite_goal:
                fav_goal = player.shorten_goal(favorite_goal)
                count = len([race for race in version_races if favorite_goal in race.row])
                if count > 1:
                    rows_text = rows_text + f'Most common goal in {version}: {fav_goal} ({count}/{len(version_races)})\n\n'
    return rows_text


def perc(small, big, decimals=1):
    return round((small / big) * 100, decimals) if big > 0 else 0

