
import plotly.graph_objs as go
from dash import dcc
## sourced from chatGPT question: "can you make a reusable dash component for a line chart"
def create_line_chart(
    x_data,
    y_data_dict,
    title="Line Chart",
    x_axis_title="X Axis",
    y_axis_title="Y Axis",
    colors=None
):
    traces = []
    for i, (label, y_data) in enumerate(y_data_dict.items()):
        trace_color = colors[i] if colors and i < len(colors) else None
        traces.append(go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines+markers",
            name=label,
            line=dict(color=trace_color)
        ))

    figure = go.Figure(data=traces)
    figure.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        template="plotly_white",
        hovermode="x unified",
        yaxis=dict(range=[0, None])
    )
    return dcc.Graph(figure=figure)
