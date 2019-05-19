import dash_table
import logging


def get_bingo_table(player, colors):

    logging.debug('Getting table for ' + player.name)
    df = player.get_pandas_table()

    table = dash_table.DataTable(

       # columns=[{}],
        data = df.to_dict('records'),

        columns = [{"name": i, "id": i} for i in df.columns],

        style_table = {
                'maxHeight' : 500
        },
        n_fixed_rows=1,
        style_header={'backgroundColor': colors['background'],
                     'color': 'white',
                      'font-family': 'Calibri'
                    },
        style_cell = {'backgroundColor' : colors['background'],
                      'color' : 'white',
                      'textAlign' : 'left',
                      'minWidth' : '100px',
                      'font-family': 'Calibri'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'minWidth': '70px'
            } for c in ['Rank', 'Entrants']

        ],

        style_as_list_view=True,

        sorting = True,

        pagination_mode = False
    )

    return table