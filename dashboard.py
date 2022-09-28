import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

binary_files_list = os.listdir('results/binary_results/')
binary_files = pd.DataFrame(os.listdir('results/binary_results/'))

app.layout = html.Div(children=[
    html.H1('ADM 1 Dashboard'),
    dash_table.DataTable(
        id='selectionTable',
        data=binary_files.to_dict('records'),
        # filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_rows=[0, 1],
        row_selectable="multi",
        page_current=0,
        page_size=10,
    ),
    dcc.Graph(id="main_plot"),
])


@app.callback(
    Output("main_plot", "figure"),
    Input('selectionTable', 'derived_virtual_selected_rows')
)
def update_bar_chart(selected_rows):
    if selected_rows is None:
        return px.bar()

    data = [list(range(1, 23))]
    dt_columns = ['query_id']

    for i in selected_rows:
        tmp = np.load('results/binary_results/%s' % binary_files_list[i])
        tmp = tmp[tmp[:, 0].argsort()]
        data_per_query = np.split(tmp[:, 1],
                                  np.unique(tmp[:, 0], return_index=True)[1][
                                  1:])
        mean_data = []
        for query_id in range(len(data_per_query)):
            if query_id == 22:
                continue
            mean_data.append(np.mean(data_per_query[query_id]))
        dt_columns.append(binary_files_list[i])
        data.append(mean_data)

    data = pd.DataFrame(np.array(data).T, columns=dt_columns)

    fig = px.bar(data, x="query_id", y=dt_columns[1:], barmode="group")
    fig.update_layout(
        title="Query Execution Time",
        xaxis_title="Query ID",
        yaxis_title="Time (seconds)",
        hovermode='x',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
