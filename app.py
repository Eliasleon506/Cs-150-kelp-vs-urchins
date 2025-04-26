
from dash import Dash, dcc, html, Input, Output
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import time

# Load data
ca_data = pd.read_csv('data/Heat data for california .csv')
sb_data = pd.read_csv('data/SB_temp.csv')
# Prepare California data


# Prepare SB data
sb_data['date'] = pd.to_datetime(sb_data['date'])
sb_data['Year'] = sb_data['date'].dt.year
sb_yearly = sb_data.groupby('Year').agg({'temp': 'mean'}).reset_index()
sb_yearly = sb_yearly[sb_yearly['Year'] >= 1982]

years = ca_data['Year']
sites = ['Trinidad Bay (°F)', 'Pacific Grove (°F)', 'La Jolla (°F)']

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Sea Urchins vs. Seaweed: Santa Barbara", className="text-center bg-primary text-white p-2"),
            html.H4("Elias Leon", className="text-center"),
            html.H4("CS-150 : Community Action Computing", className="text-center")
        ])
    ]),

    dbc.Row([
        dbc.Col(html.H1("California and Santa Barbara Ocean Temperatures (1982-2023)", className="text-center mb-4"))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='line-chart'), width=10, className="offset-md-1")
    ]),



    dbc.Row([
        dbc.Col(html.H2("Santa Barbara Detailed Ocean Temperatures", className="text-center mb-4"))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='heatmap', style={'height': '600px'}), width=10, className="offset-md-1")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='year-slider',
                min=1982,
                max=2023,
                step=1,
                value=1982,
                marks={str(year): str(year) for year in range(1982, 2024, 5)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            dbc.ButtonGroup([
                dbc.Button('Play', id='play-button', color='success', className='me-2', n_clicks=0),
                dbc.Button('Pause', id='pause-button', color='danger', n_clicks=0)
            ], className='d-flex justify-content-center')
        ], width=10, className="offset-md-1")
    ], className='my-4'),

    dcc.Interval(id='interval', interval=1000, n_intervals=0, disabled=True)
], fluid=True)

# Callbacks
@app.callback(
    Output('line-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_line_chart(selected_year):
    fig = go.Figure()
    for site in sites:
        fig.add_trace(go.Scatter(x=ca_data['Year'], y=ca_data[site], mode='lines', name=site.split(' (')[0]))
    fig.add_trace(go.Scatter(x=sb_yearly['Year'], y=sb_yearly['temp'] * 9 / 5 + 32, mode='lines', name='Santa Barbara'))

    fig.add_vrect(x0=2014, x1=2016, fillcolor="red", opacity=0.2, line_width=0, annotation_text="Marine Heatwave (2014-2016)", annotation_position="top right")
    fig.add_vrect(x0=1997, x1=1998, fillcolor="blue", opacity=0.2, line_width=0, annotation_text="El Niño (1997-1998)", annotation_position="bottom right")
    fig.add_vrect(x0=2015, x1=2016, fillcolor="blue", opacity=0.2, line_width=0, annotation_text="El Niño (2015-2016)", annotation_position="bottom left")

    fig.update_layout(
        title="Ocean Temperature Over Time",
        xaxis_title="Year",
        yaxis_title="Temperature (°F)",
        xaxis_range=[1982, 2023],
        legend_title="Location"
    )
    return fig



@app.callback(
    Output('heatmap', 'figure'),
    Input('year-slider', 'value')
)
def update_heatmap(selected_year):
    filtered_sb = sb_data[sb_data['Year'] == selected_year].copy()
    filtered_sb['temp_f'] = filtered_sb['temp'] * 9/5 + 32
    fig = px.scatter_map(
        filtered_sb,
        lat='latitude',
        lon='longitude',
        color='temp_f',
        size=[10]*len(filtered_sb),
        hover_name='site',
        size_max=20,
        zoom=8,
        center=dict(lat=34.4, lon=-119.7),
        map_style="open-street-map",
        title=f"Santa Barbara Ocean Temperature Map - {selected_year}",
        color_continuous_scale='thermal',
        range_color=[50, 65]
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text="Temperature (°F)")
        ),
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    return fig
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
if __name__ == "__main__":
    app.run(debug=True)
