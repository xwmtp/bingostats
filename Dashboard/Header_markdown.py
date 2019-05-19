import dash_core_components as dcc

def get_header_markdown(player):

    # overall stats
    all_races = player.select_races(type="bingo", forfeits=True)
    completed_races = player.select_races(type="bingo", forfeits=False)
    num_blanks = len([r for r in completed_races if r.row == 'blank'])
    num_forfeits = len([r for r in all_races if r.forfeit])


    blank_perc   = round((num_blanks   / len(completed_races)) * 100, 1) if len(completed_races) > 0 else 0
    forfeit_perc = round((num_forfeits / len(all_races))       * 100, 1) if len(all_races)       > 0 else 0

    blank_shame   = ' .shame' if blank_perc > 30 else ''
    forfeit_shame = ' .shame' if forfeit_perc > 30 else ''

    markdown_text = '# Bingo Stats {}\n\n' \
                    'Completed {} bingos.\n\n' \
                    'Blanked {} bingos ({}%).{}\n\n' \
                    'Forfeited {} bingos ({}%).{}\n\n'\
                     .format(player.name,
                             len(completed_races),
                             num_blanks, blank_perc, blank_shame,
                             num_forfeits, forfeit_perc, forfeit_shame
                             )



    return dcc.Markdown(markdown_text)
