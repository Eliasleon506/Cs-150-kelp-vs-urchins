import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
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

        # Climate events
        fig.add_vrect(x0=2014, x1=2016, fillcolor="rgba(255,0,0,0.2)", line_width=0,
                      annotation_text="The Blob (2014–2016)", annotation_position="top right")
        fig.add_vrect(x0=1997, x1=1998, fillcolor="rgba(0,0,255,0.2)", line_width=0,
                      annotation_text="El Niño (1997–1998)", annotation_position="bottom right")
        fig.add_vrect(x0=2015, x1=2016, fillcolor="rgba(0,0,255,0.2)", line_width=0,
                      annotation_text="El Niño (2015–2016)", annotation_position="bottom left")

        fig.update_layout(
            title="Ocean Temperature Over Time",
            xaxis_title="Year",
            yaxis_title="Temperature (°F)",
            xaxis_range=[1982, 2023],
            legend_title="Location"
        )

        return fig


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
        map_style="open-street-map",
        title=f"Santa Barbara Ocean Temperature Map - {selected_year}",
        color_continuous_scale='thermal',
        range_color=[50, 65]
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text="Temperature (°F)")
        ),
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
    fig.update_traces(line=dict(color="green"))
    available_years = yearly_fronds["YEAR"].tolist()
    min_year = min(available_years)
    max_year = max(available_years)

    fig.update_layout(
        yaxis_title="Total Fronds",
        xaxis_title="Year",
        xaxis_range=[min_year, max_year],  # Only zoom into real data
        yaxis_range=[0, None],
        template="plotly_white",
        hovermode="x unified"
    )
    return fig

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
    return fig


urchins_csv = pd.read_csv("data/SB_urchins.csv")
def make_urchin_linechart():

    # Group and filter
    urchin_yearly = urchins_csv[urchins_csv["COUNT"] != -99999].groupby("YEAR")["COUNT"].sum().reset_index()

    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=urchin_yearly["YEAR"], y=urchin_yearly["COUNT"],
                             mode="lines+markers", name="Urchin Count"))
    fig.update_traces(line=dict(color="Black"))
    fig.update_layout(title="Urchin Population Over Time", xaxis_title="Year", yaxis_title="Total Count")

    return fig
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
            color = "purple"
        elif "Red" in column:
            color = "red"

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
    return fig

