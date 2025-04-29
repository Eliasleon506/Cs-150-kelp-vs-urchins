from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash


from assets.Figures import make_heatmap,make_kelp_linechart, make_temp_line_chart
from assets.advanced_componets import ocean_temp
from assets.text import sea_urchin_title, student_name, course_name, main_chart_title, heatmap_title


# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2(sea_urchin_title, className="text-center bg-primary text-white p-2"),
            html.H4(student_name, className="text-center"),
            html.H4(course_name, className="text-center")
        ])
    ]),
    dbc.Row([
        dbc.Col(html.P(
            "Kelp is dying ohhh noooo. This graph shows the decline in the total number of giant kelp fronds recorded across all sampled sites over time."),
                className="text-center")
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=make_kelp_linechart()), width=10, className="offset-md-1")
    ]),

    *ocean_temp,

], fluid=True)

# Callbacks
@app.callback(
    Output('temp-line-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_line_chart(selected_year):
    return make_temp_line_chart(selected_year)

@app.callback(
    Output('heatmap', 'figure'),
    Input('year-slider', 'value')
)
def update_heatmap(selected_year):
    return make_heatmap(selected_year)

@app.callback(
    Output('interval', 'disabled'),
    [Input('play-button', 'n_clicks'), Input('pause-button', 'n_clicks')],
    State('interval', 'disabled')
)
def toggle_interval(play_clicks, pause_clicks, disabled):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'play-button' in changed_id:
        return False
    elif 'pause-button' in changed_id:
        return True
    return disabled

@app.callback(
    Output('year-slider', 'value'),
    Input('interval', 'n_intervals'),
    State('year-slider', 'value')
)
def update_slider(n_intervals, current_year):
    if current_year < 2023:
        return current_year + 1
    else:
        return 1982

# Run server
if __name__ == '__main__':
    app.run(debug=True)

