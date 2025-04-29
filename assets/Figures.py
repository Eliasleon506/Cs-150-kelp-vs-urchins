import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

# Load data once
ca_data = pd.read_csv('data/Heat data for california .csv')
sb_data = pd.read_csv('data/SB_temp.csv')

# Preprocess Santa Barbara data
sb_data['date'] = pd.to_datetime(sb_data['date'])
sb_data['Year'] = sb_data['date'].dt.year
sb_yearly = sb_data.groupby('Year').agg({'temp': 'mean'}).reset_index()
sb_yearly = sb_yearly[sb_yearly['Year'] >= 1982]

sites = ['Trinidad Bay (°F)', 'Pacific Grove (°F)', 'La Jolla (°F)']

def make_line_chart(selected_year=None):
    fig = go.Figure()
    for site in sites:
        fig.add_trace(go.Scatter(x=ca_data['Year'], y=ca_data[site], mode='lines', name=site.split(' (')[0]))
    fig.add_trace(go.Scatter(x=sb_yearly['Year'], y=sb_yearly['temp'] * 9 / 5 + 32, mode='lines', name='Santa Barbara'))

    fig.add_vrect(x0=2014, x1=2016, fillcolor="red", opacity=0.2, line_width=0,
                  annotation_text="Marine Heatwave (2014-2016)", annotation_position="top right")
    fig.add_vrect(x0=1997, x1=1998, fillcolor="blue", opacity=0.2, line_width=0,
                  annotation_text="El Niño (1997-1998)", annotation_position="bottom right")
    fig.add_vrect(x0=2015, x1=2016, fillcolor="blue", opacity=0.2, line_width=0,
                  annotation_text="El Niño (2015-2016)", annotation_position="bottom left")

    fig.update_layout(
        title="Ocean Temperature Over Time",
        xaxis_title="Year",
        yaxis_title="Temperature (°F)",
        xaxis_range=[1982, 2023],
        legend_title="Location"
    )
    return fig

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
