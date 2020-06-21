from Dashboard.Plots.Layout import colors
import dash_table
import pandas as pd


def get_bingo_table(player=None):
    if player:
        df = player.get_pandas_table()
    else:
        df = pd.DataFrame()

    table = dash_table.DataTable(

       # columns=[{}],
        data = df.to_dict('records'),

        columns = [{"name": i, "id": i} for i in df.columns],

        style_table = {
                'maxHeight' : 500,
                'overflowX' : 'auto'
        },

        style_cell = {'backgroundColor' : colors['background'],
                      'color' : colors['text'],
                      'textAlign' : 'left',
                      'minWidth' : '130px',
                      'font-family': 'Calibri'
        },
        style_cell_conditional =
            [{'if': {'column_id': c}, 'minWidth' : '90px', 'width' : '90px', 'maxWidth' : '90px'} for c in ['Date']] +
            [{'if': {'column_id': c}, 'minWidth' : '75px', 'width' : '75px', 'maxWidth' : '75px'} for c in ['Type']] +
            [{'if': {'column_id': c}, 'minWidth' : '55px', 'width' : '55px', 'maxWidth' : '55px'} for c in ['Rank']] +
            [{'if': {'column_id': c}, 'minWidth' : '90px', 'width' : '90px', 'maxWidth' : '90px'} for c in ['SRL-id']] +
            [{'if': {'column_id': c}, 'minWidth' : '65px',  'width': '65px', 'maxWidth' : '65px'} for c in ['Time', 'SRL-id']],

        sort_action = 'native',

        style_as_list_view=True,

        page_action = 'none',

        export_format = 'csv'
    )

    return table