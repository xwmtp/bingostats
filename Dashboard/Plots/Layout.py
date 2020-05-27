import plotly.graph_objs as go

colors = {
    'background': '#111111',
    'title': '#e09456',
    'text': '#bec7d2'
}

def get_graph_layout(title, height, y_label='Time', tickformat='%-Hh%M'):
    return go.Layout(
        title={'text': title, 'font': {'color': colors['title']}},
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={
            'color': colors['text']
        },
        height=height,
        xaxis={'title': 'Date', 'gridcolor': '#222222', 'linecolor': '#333333'},
        yaxis={'title': y_label, 'gridcolor': '#222222', 'linecolor': '#333333', 'tickformat': tickformat},
        margin={'l': 75, 'b': 50, 't': 150, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )