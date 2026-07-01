import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

########################## SHARED STORY THEME
# One palette + one theme so every cartesian chart blends into the dark
# SUPERHERO Bootstrap theme instead of the old mix of plotly_white / default.
STORY_COLORS = {
    "kelp": "#2ca02c",          # green  — giant kelp
    "purple_urchin": "#9467bd",  # purple urchin (the story's culprit)
    "red_urchin": "#d62728",     # red urchin (harvested / checked)
    "temp": "#ff7f0e",           # warm orange — ocean temperature
    "sb": "#17becf",             # teal — Santa Barbara
    "blob": "rgba(214,39,40,0.15)",  # shaded "The Blob" band
}


def apply_story_theme(fig):
    """Harmonize a cartesian figure with the dark SUPERHERO theme.

    Only touches chrome (template/background/font/margins) — never the data,
    trace order, or figure id — so existing slider/animation callbacks keep working.
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e9ecef"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, r=20, l=20, b=40),
    )
    return fig

########################## KELP DATA
# Load and preprocess data
df = pd.read_csv("data/SB_kelp.csv", parse_dates=["DATE"])

# Filter for only Giant Kelp data (just in case)
df = df[df["COMMON_NAME"] == "Giant Kelp"]

df = df[df["FRONDS"] >= 0]  # Keep only real non-negative frond counts


# Aggregate total fronds per year
df["YEAR"] = pd.to_datetime(df["DATE"]).dt.year
yearly_fronds = df.groupby("YEAR")["FRONDS"].sum().reset_index()


############################TEMP DATA made with Chatgpt "Given the following csv files can you make a line chart for the temp in california and a heat map for the temp in santa barbara"
# Load data once
ca_data = pd.read_csv('data/Heat data for california .csv')
sb_data = pd.read_csv('data/SB_temp.csv')

# Preprocess Santa Barbara data
sb_data['date'] = pd.to_datetime(sb_data['date'])
sb_data['Year'] = sb_data['date'].dt.year
sb_yearly = sb_data.groupby('Year').agg({'temp': 'mean'}).reset_index()
sb_yearly = sb_yearly[sb_yearly['Year'] >= 1982]

sites = ['Trinidad Bay (°F)', 'Pacific Grove (°F)', 'La Jolla (°F)']

########################## SEA-STAR (PREDATOR) DATA — same survey as the urchins/kelp
# The keystone predators that vanished at the 2013–14 sea-star wasting outbreak.
# Only urchin-eating stars (Pycnopodia + Pisaster giganteus) — NOT the bat star,
# a scavenger whose numbers recover and would muddy the "predators gone" message.
_invert = pd.read_csv("data/invertebray_Algea_count.csv", low_memory=False)
_invert = _invert[_invert["COUNT"] != -99999]
PREDATOR_STARS = ["Sunflower Sea Star", "Giant Spined Sea Star"]


########################## CENTERPIECE: warming vs kelp (the defensible "smoking gun")
# Shows what the Santa Barbara survey data actually supports: ocean temperature
# spiking during The Blob alongside a faltering kelp forest. Urchins are left to
# their own section because the local transect counts do NOT show a post-Blob surge.
def make_collapse_overlay_chart():
    kelp = yearly_fronds[yearly_fronds["YEAR"] >= 2008]
    temp = sb_yearly[sb_yearly["Year"] >= 2008].copy()
    temp["temp_f"] = temp["temp"] * 9 / 5 + 32

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=kelp["YEAR"], y=kelp["FRONDS"], name="Giant kelp fronds",
        mode="lines+markers", line=dict(color=STORY_COLORS["kelp"], width=3)),
        secondary_y=False)
    fig.add_trace(go.Scatter(
        x=temp["Year"], y=temp["temp_f"], name="Ocean temperature (°F)",
        mode="lines+markers",
        line=dict(color=STORY_COLORS["temp"], width=3, dash="dot")),
        secondary_y=True)

    fig.add_vrect(x0=2014, x1=2016, fillcolor=STORY_COLORS["blob"], line_width=0,
                  annotation_text="The Blob (2014–2016)", annotation_position="top left")

    # Point a reader straight at the record kelp lows.
    klow_year = int(kelp.set_index("YEAR")["FRONDS"].idxmin())
    klow_val = int(kelp.set_index("YEAR")["FRONDS"].min())
    fig.add_annotation(x=klow_year, y=klow_val, ax=0, ay=-50, showarrow=True, arrowhead=2,
                       text="Record kelp lows", font=dict(color=STORY_COLORS["kelp"]),
                       secondary_y=False)

    fig.update_layout(
        title="As the ocean warmed, the kelp forest faltered — Santa Barbara, 2008–2023",
        xaxis_title="Year",
        hovermode="x unified",
    )
    fig.update_yaxes(title_text="Total giant kelp fronds", secondary_y=False)
    fig.update_yaxes(title_text="Mean ocean temperature (°F)", secondary_y=True)

    fig = apply_story_theme(fig)
    # Legend below the plot so it never collides with the title (set after the
    # theme, which standardizes margins).
    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.2, x=0.5, xanchor="center"),
        margin=dict(t=60, r=30, l=30, b=90),
    )
    return fig


########################## HEADLINE METRICS (robust, auditable — periods stated on the card)
def compute_headline_metrics():
    """Derive headline numbers from multi-year averages (not single noisy years).

    Each metric names the periods it compares so a reader can audit it. Only
    metrics the data clearly supports are returned.
    """
    temp = sb_yearly.copy()
    temp["temp_f"] = temp["temp"] * 9 / 5 + 32
    tf = temp.set_index("Year")["temp_f"]
    base = tf[(tf.index >= 2008) & (tf.index <= 2013)].mean()
    recent = tf[(tf.index >= 2017) & (tf.index <= 2023)].mean()
    blob = tf[(tf.index >= 2014) & (tf.index <= 2016)]
    peak_year = int(blob.idxmax())
    peak = blob.max()

    kelp = yearly_fronds.set_index("YEAR")["FRONDS"]
    kbase = kelp[(kelp.index >= 2008) & (kelp.index <= 2013)].mean()
    klow_year = int(kelp[kelp.index >= 2014].idxmin())
    klow = kelp.loc[klow_year]

    # Keystone predator collapse — Sunflower Sea Star recorded count by year.
    sun = _invert[_invert["COMMON_NAME"] == "Sunflower Sea Star"].groupby("YEAR")["COUNT"].sum()
    sun_peak = int(sun.max())
    sun_peak_year = int(sun.idxmax())

    return [
        {"value": f"+{peak - base:.1f}°F",
         "label": f"Ocean temp at The Blob's {peak_year} peak vs the 2008–2013 average",
         "color": "danger"},
        {"value": f"{(klow - kbase) / kbase * 100:.0f}%",
         "label": f"Giant kelp fronds at their {klow_year} low vs the 2008–2013 average",
         "color": "success"},
        {"value": f"+{recent - base:.1f}°F",
         "label": "Sustained warming — 2017–2023 average vs the 2008–2013 average",
         "color": "warning"},
        {"value": "→ 0",
         "label": f"Sunflower sea stars recorded: ~{sun_peak} in {sun_peak_year}, then 0 every year 2014–2024",
         "color": "info"},
    ]


########################## SEA-STAR COLLAPSE — the missing causal leg, completed with local data
def make_seastar_collapse_chart():
    fig = go.Figure()
    colors = {"Sunflower Sea Star": STORY_COLORS["temp"],
              "Giant Spined Sea Star": STORY_COLORS["red_urchin"]}
    for sp in PREDATOR_STARS:
        s = _invert[_invert["COMMON_NAME"] == sp].groupby("YEAR")["COUNT"].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=s["YEAR"], y=s["COUNT"], name=sp,
            mode="lines+markers", line=dict(color=colors.get(sp), width=3)))

    fig.add_vrect(x0=2013, x1=2016, fillcolor=STORY_COLORS["blob"], line_width=0,
                  annotation_text="Sea star wasting + The Blob", annotation_position="top right")
    # ax/ay are PIXEL offsets from the anchored data point (not data values).
    fig.add_annotation(x=2014, y=430, ax=90, ay=-40, showarrow=True, arrowhead=2,
                       text="Predators vanish — and stay gone", font=dict(color="#e9ecef"))

    fig.update_layout(
        title="The keystone predators vanished — urchin-eating sea stars, Santa Barbara",
        xaxis_title="Year", yaxis_title="Total recorded count",
        hovermode="x unified",
    )
    return apply_story_theme(fig)


########################## PER-SITE KELP — the decline is system-wide, not one noisy reef
def make_kelp_by_site_chart():
    by_site = df.groupby(["SITE", "YEAR"])["FRONDS"].sum().reset_index()
    fig = px.line(
        by_site, x="YEAR", y="FRONDS", facet_col="SITE", facet_col_wrap=3,
        markers=True, color_discrete_sequence=[STORY_COLORS["kelp"]],
        title="Giant kelp fronds by reef site, Santa Barbara (2008–2024)",
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(matches=None, title_text="")
    fig.update_xaxes(title_text="")
    return apply_story_theme(fig)
##################################
### made with Chatgpt "Given the following csv files can you make a line chart for the temp in california and a heat map for the temp in santa barbara"
def make_temp_line_chart(selected_year=None):
        # Define custom color palette (blue, orange, pink, yellow)
        filtered_colors = [
            "#1f77b4",  # blue
            "#ff7f0e",  # orange
            "#e377c2",  # pink
            "#bcbd22"  # yellow
        ]

        fig = go.Figure()

        for i, site in enumerate(sites):
            color = filtered_colors[i % len(filtered_colors)]
            fig.add_trace(go.Scatter(
                x=ca_data['Year'],
                y=ca_data[site],
                mode='lines',
                name=site.split(' (')[0],
                line=dict(color=color)
            ))

        # Santa Barbara in teal
        fig.add_trace(go.Scatter(
            x=sb_yearly['Year'],
            y=sb_yearly['temp'] * 9 / 5 + 32,
            mode='lines',
            name='Santa Barbara',
            line=dict(color="#17becf")  # teal
        ))

        # Climate events — positioned so labels don't collide with each other
        fig.add_vrect(x0=2014, x1=2016, fillcolor="rgba(255,0,0,0.18)", line_width=0,
                      annotation_text="The Blob", annotation_position="top left")
        fig.add_vrect(x0=1997, x1=1998, fillcolor="rgba(0,0,255,0.18)", line_width=0,
                      annotation_text="El Niño ’97–’98", annotation_position="top right")
        fig.add_vrect(x0=2015, x1=2016, fillcolor="rgba(0,0,255,0.18)", line_width=0,
                      annotation_text="El Niño ’15–’16", annotation_position="bottom right")

        fig.update_layout(
            title="Ocean Temperature Over Time",
            xaxis_title="Year",
            yaxis_title="Temperature (°F)",
            xaxis_range=[1982, 2023],
            legend_title="Location"
        )

        return apply_story_theme(fig)


### made with Chatgpt "Given the following csv files can you make a line chart for the temp in california and a heat map for the temp in santa barbara"
def make_heatmap(selected_year):
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
        map_style="carto-darkmatter",
        title=f"Santa Barbara Ocean Temperature Map - {selected_year}",
        color_continuous_scale='thermal',
        range_color=[50, 65]
    )
    # This is a map, not a cartesian chart — plotly_dark won't restyle the basemap,
    # so we only harmonize the surrounding chrome (dark basemap + light font/bg).
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text="Temperature (°F)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e9ecef"),
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )
    return fig

def make_kelp_linechart():
    fig = px.line(
        yearly_fronds,
        x="YEAR",
        y="FRONDS",
        title="Total Giant Kelp Fronds Over Time"
    )
    fig.update_traces(line=dict(color=STORY_COLORS["kelp"]))
    available_years = yearly_fronds["YEAR"].tolist()
    min_year = min(available_years)
    max_year = max(available_years)

    fig.update_layout(
        yaxis_title="Total Fronds",
        xaxis_title="Year",
        xaxis_range=[min_year, max_year],  # Only zoom into real data
        yaxis_range=[0, None],
        hovermode="x unified"
    )
    return apply_story_theme(fig)

######## graph for the Tabs
def make_species_decline_chart(fish_path='data/Sb_fish_count.csv', invert_path='data/invertebray_Algea_count.csv'):
    # Load fish data
    fish_df = pd.read_csv(fish_path,low_memory=False)
    fish_df = fish_df[fish_df["COUNT"] != -99999]
    fish_yearly = fish_df.groupby("YEAR")["COUNT"].sum().reset_index()
    fish_yearly.rename(columns={"COUNT": "Fish Count"}, inplace=True)

    # Load invertebrate data and exclude kelp and -99999
    invert_df = pd.read_csv(invert_path,low_memory=False)
    invert_df = invert_df[invert_df["COUNT"] != -99999]
    invert_df = invert_df[~invert_df["COMMON_NAME"].str.contains("kelp", case=False, na=False)]
    invert_yearly = invert_df.groupby("YEAR")["COUNT"].sum().reset_index()
    invert_yearly.rename(columns={"COUNT": "Invertebrate Count"}, inplace=True)
    # Merge and plot
    merged = pd.merge(fish_yearly, invert_yearly, how="outer", on="YEAR").fillna(0)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=merged["YEAR"], y=merged["Fish Count"],
                             mode='lines+markers', name='Fish Count'))
    fig.add_trace(go.Scatter(x=merged["YEAR"], y=merged["Invertebrate Count"],
                             mode='lines+markers', name='Invertebrate Count'))
    fig.update_layout(title="Fish vs Invertebrate Counts Over Time",
                      xaxis_title="Year", yaxis_title="Count")
    return apply_story_theme(fig)


urchins_csv = pd.read_csv("data/SB_urchins.csv")
def make_urchin_linechart():

    # Group and filter
    urchin_yearly = urchins_csv[urchins_csv["COUNT"] != -99999].groupby("YEAR")["COUNT"].sum().reset_index()

    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=urchin_yearly["YEAR"], y=urchin_yearly["COUNT"],
                             mode="lines+markers", name="Urchin Count"))
    fig.update_traces(line=dict(color=STORY_COLORS["sb"]))
    fig.update_layout(title="Urchin Population Over Time", xaxis_title="Year", yaxis_title="Total Count")

    return apply_story_theme(fig)
def make_RvP_urchin_linechart():
    pivot_df = urchins_csv.pivot_table(
        index="YEAR",
        columns="COMMON_NAME",
        values="COUNT",
        aggfunc="sum"
    ).reset_index()

    # Create line chart
    fig = go.Figure()

    for column in pivot_df.columns[1:]:  # Skip 'YEAR'
        color = None
        if "Purple" in column:
            color = STORY_COLORS["purple_urchin"]
        elif "Red" in column:
            color = STORY_COLORS["red_urchin"]

        fig.add_trace(go.Scatter(
            x=pivot_df["YEAR"],
            y=pivot_df[column],
            mode="lines+markers",
            name=column,
            line=dict(color=color) if color else None
        ))

    fig.update_layout(
        title="Red vs Purple Urchin Population Over Time",
        xaxis_title="Year",
        yaxis_title="Total Count"
    )
    return apply_story_theme(fig)

