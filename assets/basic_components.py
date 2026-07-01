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


def stat_card(value, label, color="primary"):
    """A headline number with an auditable caption (the compared periods)."""
    return dbc.Card(
        dbc.CardBody([
            html.H2(value, className=f"text-{color} fw-bold mb-1"),
            html.P(label, className="text-muted small mb-0"),
        ]),
        className="text-center h-100 shadow-sm",
    )


def section_header(title):
    """Consistent section heading with a divider so the long scroll has rhythm."""
    return html.H4(title, className="mt-5 mb-3 pb-2 border-bottom border-secondary")


def anchor(anchor_id):
    """Invisible scroll target that clears the sticky navbar (scroll-margin-top)."""
    return html.Div(id=anchor_id, style={"scrollMarginTop": "80px"})


def callout(quote, source=None):
    """Pull-quote that visually elevates a sentence (verbatim — no rewriting)."""
    body = [html.P(quote, className="mb-0 fs-5 fst-italic")]
    if source:
        body.append(html.Footer(source, className="blockquote-footer mt-2"))
    return dbc.Card(
        dbc.CardBody(body),
        className="story-callout border-start border-info border-4 my-4",
    )


def link_button(label, href):
    """Styled outline button link (replaces bare <a> URLs)."""
    return dbc.Button(label, href=href, target="_blank",
                      color="info", outline=True, size="sm",
                      className="me-2 mb-2")


def sources_footer():
    """Consolidated citations + an honest methods/caveat note."""
    refs = [
        ("Data: Santa Barbara Coastal LTER (kelp, urchins, sea stars, temperature)",
         "https://sbclter.msi.ucsb.edu/"),
        ("Environmental Data Initiative (EDI) data portal",
         "https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc"),
        ("Sunflower Star Lab",
         "https://www.sunflowerstarlab.org/"),
        ("L.A. Times — sunflower sea star & kelp restoration",
         "https://www.latimes.com/environment/story/2025-04-11/sunflower-sea-star-restoring-kelp-forests"),
        ("The Independent — returning the kelp forest",
         "https://www.independent.com/2023/12/20/mission-possible-returning-the-kelp-forest-to-our-coast/"),
        ("PBS — Santa Barbara purple urchin project",
         "https://www.independent.com/2024/06/10/pbs-focuses-on-santa-barbaras-purple-urchin-project/"),
    ]
    return html.Footer([
        html.Hr(className="mt-5"),
        dbc.Row(dbc.Col([
            html.H5("Data Sources & Methods", className="mb-3"),
            html.P(
                "Kelp, urchin, sea-star and reef-temperature figures come from the "
                "Santa Barbara Coastal LTER diver surveys at five reef sites "
                "(AQUE, MOHK, NAPL, CARP, IVEE), with statewide temperatures from the "
                "California temperature record. Counts are raw survey totals, so a single "
                "year can be noisy; the headline numbers compare multi-year averages. Note "
                "that fixed-transect surveys can under-sample urchin “barrens,” which often "
                "form outside the survey plots — so local purple-urchin counts may understate "
                "the regional surge described in the literature.",
                className="small text-muted",
            ),
            html.Ul([html.Li(html.A(label, href=url, target="_blank")) for label, url in refs],
                    className="small"),
        ], width=10, className="offset-md-1")),
    ], className="mt-5 mb-4")


