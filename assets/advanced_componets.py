from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from assets.basic_components import make_slider, make_button_group
from assets.text import sea_urchin_title, student_name, course_name, main_chart_title, heatmap_title


ocean_temp = [
    dbc.Row([
        dbc.Col(html.H1(main_chart_title, className="text-center mb-4"))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='temp-line-chart'), width=10, className="offset-md-1")
    ]),
    dbc.Row([
        dbc.Col(html.H2(heatmap_title, className="text-center mb-4"))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='heatmap', style={'height': '600px'}), width=10, className="offset-md-1")
    ]),
    dbc.Row([
        dbc.Col([
           make_slider(),
           html.Br(),
           make_button_group()
        ], width=10, className="offset-md-1")
    ], className='my-4'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0, disabled=True)
]
