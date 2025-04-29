from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash


from assets.Figures import make_line_chart, make_heatmap
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
    *ocean_temp,

], fluid=True)

# Callbacks
@app.callback(
    Output('temp-line-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_line_chart(selected_year):
    return make_line_chart(selected_year)

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

