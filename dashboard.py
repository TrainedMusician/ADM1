import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import os

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

binary_files_list = os.listdir('results/binary_results/')
binary_files_list.sort()
binary_files = pd.DataFrame(binary_files_list)
data_q1 = pd.read_csv('results/q1.csv')
data_q6 = pd.read_csv('results/q6.csv')
fig_q1 = px.bar(data_q1, x='Machine', y='Time (s)', color='Process', title='Q1 Implementation')
fig_q6 = px.bar(data_q6, x='Machine', y='Time (s)', color='Process', title='Q6 Implementation (Python & R)')

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
    daq.ToggleSwitch(
        id='main_log',
        value=False,
        label='Log10 Y-axis',
        labelPosition='top'
    ),
    dcc.Graph(id="main_plot"),
    dcc.Graph(figure=fig_q1),
    dcc.Graph(figure=fig_q6),
])


@app.callback(
    Output("main_plot", "figure"),
    Input('selectionTable', 'derived_virtual_selected_rows'),
    Input('main_log', 'value')
)
def update_bar_chart(selected_rows, log_active):
    if selected_rows is None:
        return px.bar()

    # selected_rows.sort()
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

    y_axis = "Time (seconds)"
    if log_active:
        y_axis += ' log10 scale'

    fig = px.bar(data, x="query_id", y=dt_columns[1:], barmode="group", log_y=log_active)
    fig.update_layout(
        title="Query Execution Time",
        xaxis_title="Query ID",
        yaxis_title=y_axis,
        hovermode='x',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
