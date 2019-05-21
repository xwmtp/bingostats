import dash_core_components as dcc
import logging

def get_stats_text(player, input):

    # overall stats
    all_races = player.select_races(type="bingo", forfeits=True)
    completed_races = player.select_races(type="bingo", forfeits=False)
    blank_races = [r for r in completed_races if r.type != 'v2' and r.type != 'v3'] #posting rows was not really a thing in v2/3
    num_blanks = len([r for r in blank_races if r.row_id == 'blank'])
    num_forfeits = len([r for r in all_races if r.forfeit])


    blank_perc   = round((num_blanks   / len(blank_races)) * 100, 1) if len(completed_races) > 0 else 0
    forfeit_perc = round((num_forfeits / len(all_races))   * 100, 1) if len(all_races)       > 0 else 0

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
        text = '# ' + player.name + '\n\n' \
               'Completed {} bingos.\n\n' \
               'Blanked {} bingos ({}%).{}\n\n' \
               'Forfeited {} bingos ({}%).{}\n\n'\
               .format(len(completed_races),
                       num_blanks, blank_perc, blank_shame,
                       num_forfeits, forfeit_perc, forfeit_shame
               )



    return dcc.Markdown(text)
