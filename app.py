from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash


from assets.Figures import make_heatmap, make_kelp_linechart, make_temp_line_chart, make_species_decline_chart, \
    make_urchin_linechart, compute_headline_metrics
from assets.advanced_componets import ocean_temp, falling_kelp, co2_card, tab1_content, Urchins_total, Urchins_VS, \
    tab_predators, tab_harvesting, tab_replanting, restoration_card
from assets.basic_components import stat_card, sources_footer
from assets.text import sea_urchin_title, student_name, course_name


# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

# Sticky section navigation (anchors live in assets/advanced_componets.py)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Intro", href="#intro", external_link=True)),
        dbc.NavItem(dbc.NavLink("Why care", href="#why-care", external_link=True)),
        dbc.NavItem(dbc.NavLink("Warming", href="#why-suffering", external_link=True)),
        dbc.NavItem(dbc.NavLink("Kelp vs Urchins", href="#kelp-vs-urchins", external_link=True)),
        dbc.NavItem(dbc.NavLink("Red vs Purple", href="#red-vs-purple", external_link=True)),
        dbc.NavItem(dbc.NavLink("How to help", href="#how-to-help", external_link=True)),
    ],
    brand="Sea Urchins vs. Seaweed",
    color="primary", dark=True, sticky="top", fluid=True,
)

# Headline stat cards (numbers computed from the data, periods stated on each card)
stat_row = dbc.Row(
    [dbc.Col(stat_card(m["value"], m["label"], m["color"]), md=6, lg=3, className="mb-3")
     for m in compute_headline_metrics()],
    className="g-3 mb-5", justify="center",
)

# Layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                html.H2(sea_urchin_title, className="text-center bg-primary text-white p-2"),
                html.H4(student_name, className="text-center"),
                html.H4(course_name, className="text-center"),

                ],className= "mb-4")
            ])
        ]),

        dbc.Row(dbc.Col(stat_row, width=10, className="offset-md-1")),

        *falling_kelp
        ,
        *co2_card,
        *ocean_temp,
        *Urchins_total,
        *Urchins_VS,
        *restoration_card,

        sources_footer(),

    ], fluid=True)
])

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

@app.callback(
    Output("co2-tab-content", "children"),
    Input("co2-tabs", "active_tab")
)
def update_co2_tab(tab):
    if tab == "tab-1":
        return tab1_content
    elif tab == "tab-2":
        fig = make_species_decline_chart()
        return dbc.CardBody([
            html.H4("Species Decline Over Time", className="card-title"),
            html.P("Fish and invertebrate counts by year (excluding kelp)."),
            dcc.Graph(figure=fig)
        ])

# Callback to render content per restoration tab
@app.callback(
    Output("restoration-tab-content", "children"),
    Input("restoration-tabs", "active_tab")
)
def update_restoration_tab(active_tab):
    if active_tab == "tab-predators":
        return tab_predators
    elif active_tab == "tab-harvest":
        return tab_harvesting
    elif active_tab == "tab-replant":
        return tab_replanting
    return html.P("Tab not found.")

# Run server
if __name__ == '__main__':
    app.run(debug=True)

