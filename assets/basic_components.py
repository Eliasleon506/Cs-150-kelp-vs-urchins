from dash import dcc, html
import dash_bootstrap_components as dbc

def make_slider():
    return dcc.Slider(
        id='year-slider',
        min=1982,
        max=2023,
        step=1,
        value=1982,
        marks={str(year): str(year) for year in range(1982, 2024, 5)},
        tooltip={"placement": "bottom", "always_visible": True}
    )


def make_button_group():
    return dbc.ButtonGroup([
        dbc.Button('Play', id='play-button', color='success', className='me-2', n_clicks=0),
        dbc.Button('Pause', id='pause-button', color='danger', n_clicks=0)
    ], className='d-flex justify-content-center')

def card_component(title, children):
    return dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody(children)
    ])


