import plotly.graph_objects as go

def plot_bar(data, variable, colour='cadetblue'):
    """Plot bar chart of a single variable."""
    
    mapping = {'month': 'Month', 'day_of_week': 'Day of the Week', 
               'hour': 'Hour', 'parking_zone': 'Parking Zone'}
    
    grouped_data = data.groupby(by=variable).size().reset_index(name="Count")

    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
        x = grouped_data[variable],
        y = grouped_data['Count'],
        marker_color=colour
        )
    )

    fig.update_layout(
        title="",
        xaxis_title=mapping.get(variable),
        yaxis_title="Number of Parking Sessions")

    fig.show()


def plot_heatmap(data, variable1, variable2, colorscale="Purples"):
    """Plot heatmap of two variables."""
    
    mapping = {'month': 'Month', 'day_of_week': 'Day of the Week', 
               'hour': 'Hour', 'parking_zone': 'Parking Zone'}
    
    heatmap_data = data.groupby(by=[variable1, variable2])["date"].count().to_frame('Count').reset_index()
    heatmap_data = heatmap_data.pivot(index=variable1, columns=variable2, values="Count")

    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=colorscale))

    fig.update_layout(
        title="",
        xaxis_title=mapping.get(variable2),
        yaxis_title=mapping.get(variable1), 
        xaxis_nticks=36)

    fig.show()