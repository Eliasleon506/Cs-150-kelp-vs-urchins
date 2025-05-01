from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash

from assets.basic_components import make_slider, make_button_group
from assets.text import intro_title, intro_p, C02, main_chart_title, heatmap_title, predators, divers, replanting, \
    heat_wave, sunflower_p, kelp_lose_p, kelpVurchins, red_vs_purple, helping_p
from assets.Figures import make_kelp_linechart, make_urchin_linechart, make_RvP_urchin_linechart

falling_kelp = [
    dbc.Row(dbc.Col(html.H4(intro_title),width=10,className="offset-md-1")),
    dbc.Row(dbc.Col(html.H5(intro_p),width=10, className="offset-md-1")),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=make_kelp_linechart()), width=10, className="offset-md-1")
    ])

]


######3 CO2 and Kelp tab (static content)
tab1_content = dbc.CardBody([
    html.H4("CO₂ and Kelp Forests", className="card-title"),
    html.P(C02),
])

# Tab 2 will be rendered in callback with chart
tab2_container = dbc.CardBody(id="co2-tab-content")

# This card component is imported in app.py
co2_card = [
    html.Div(className= "mt-5"),
    dbc.Row(dbc.Col([
        html.H4("Why we should care"),
        html.P(kelp_lose_p)
    ],width=10,className="offset-md-1")),
    dbc.Row(dbc.Col(dbc.Card([
    dbc.CardHeader(
        dbc.Tabs([
            dbc.Tab(label="CO₂ and Kelp", tab_id="tab-1"),
            dbc.Tab(label="Species Decline", tab_id="tab-2"),
        ], id="co2-tabs", active_tab="tab-1")
    ),
    tab2_container
], className="my-4")
,width=10,className="offset-md-1"))]

Urchins_total = ([
    dbc.Row(dbc.Col([
        html.H4("Kelp vs Urchins"),
        html.P(kelpVurchins)], width=10, className="offset-md-1"
    )),
    dbc.Row([
    dbc.Col(
        dcc.Graph(figure=make_urchin_linechart()),
        width=5,className="offset-md-1"),
    dbc.Col(
        dcc.Graph(figure=make_kelp_linechart()),
        width=5,className="mb-5"),
])])
Urchins_VS = ([
    dbc.Row(dbc.Col([
        html.H4("Red Vs Purple"),
        html.P(red_vs_purple)], width=10, className="offset-md-1"
    )),
    dbc.Row(dbc.Col(dcc.Graph(figure=make_RvP_urchin_linechart()),width=10,className="offset-md-1", ))
])


ocean_temp = [
    dbc.Row(dbc.Col([
        html.H4("Why is the Kelp suffering?"),
        html.P(heat_wave)], width=10, className="offset-md-1"
    )),
    dbc.Row([
        dbc.Col(html.H4(main_chart_title, className="text-center mb-4"))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='temp-line-chart'), width=10, className="offset-md-1")
    ]),
    dbc.Row([
        dbc.Col([html.H4(heatmap_title, className="text-center mb-4"),
                html.P("To explore with more detail how water temperature has changed in different areas in Santa Barbara",className="text-center mb-4")])
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
    dcc.Interval(id='interval', interval=1000, n_intervals=0, disabled=True),

    dbc.Row(dbc.Col([
        html.H5("Sunflower Sea Star"),
        html.P(sunflower_p),

        html.Img(
            src="https://ca-times.brightspotcdn.com/dims4/default/82d14c3/2147483647/strip/true/crop/8192x5460+0+2/resize/2000x1333!/format/webp/quality/75/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F03%2Fc7%2F55a3332744f98d6eb0fb6fcd6994%2Fnw-wa-by-marco-mazza.jpg"
            ,style={"width": "50%","height": "auto", "display": "block", "margin": "0 auto"}),
        html.P("Source: https://www.latimes.com/environment/story/2025-04-11/sunflower-sea-star-restoring-kelp-forests",className="text-center mb-4")

    ], width=10, className="offset-md-1",

    )),
]


# Placeholder tab contents
tab_predators = dbc.CardBody([
    html.H4("Protect and Bring Back Predators", className="card-title"),
    html.P(predators),
    html.A("Sunflower Starfish Project", href="https://www.sunflowerstarlab.org/", target="_blank"),
])

tab_harvesting = dbc.CardBody([
    html.H4("Incentivize Urchin Harvesting", className="card-title"),
    html.P(divers),
    html.A("Support local Purple Urchin farming",
           href="https://www.culturedabalone.com/shop/purple-hotchi-sea-urchin/JYBIGJTLPOLYO2UBBCROLILX",
           target="_blank"),
    html.Br(),
    html.A("L.A. Times article", href="https://www.latimes.com/food/story/2022-03-03/from-plague-to-delicacy-reconsidering-purple-sea-urchin", target="_blank"),
    html.Br(),
    html.A("PBS Focus on Santa Barbara", href="https://www.independent.com/2024/06/10/pbs-focuses-on-santa-barbaras-purple-urchin-project/", target="_blank"),
])

tab_replanting = dbc.CardBody([
    html.H4("Kelp Replanting Efforts", className="card-title"),
    html.P(replanting),
    html.A("Independent article on kelp restoration", href="https://www.independent.com/2023/12/20/mission-possible-returning-the-kelp-forest-to-our-coast/", target="_blank"),
])

# The card with 3 tabs
restoration_card = ([
    dbc.Row(dbc.Col([
        html.Div([
        html.H4("How we can help!!"),
        html.P(helping_p)
        ],className="mt-5")
        ],width=10, className="offset-md-1"
    )
    ),
    dbc.Row(dbc.Col([
    dbc.Card([
    dbc.CardHeader(
        dbc.Tabs([
            dbc.Tab(label="Predators", tab_id="tab-predators"),
            dbc.Tab(label="Urchin Harvesting", tab_id="tab-harvest"),
            dbc.Tab(label="Replanting Kelp", tab_id="tab-replant"),
        ], id="restoration-tabs", active_tab="tab-predators")
    ),
    dbc.CardBody(id="restoration-tab-content")
], className="my-4")],width=10,className="offset-md-1"),)]
)

