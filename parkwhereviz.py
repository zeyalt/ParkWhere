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
    # py.plot(fig, filename="by_" + variable, auto_open=True)

def plot_stacked_bar(data, primary_var, stacking_var, by_percentage=False):
    
    if by_percentage:
        grouped_data = data.groupby(by=[primary_var, stacking_var]).size()\
                            .groupby(level=0)\
                            .apply(lambda x: round(100 * x / float(x.sum()), 1))\
                            .reset_index(name="Count")
        yaxis_label = "Percentage of Parking Sessions (%)"
    
    else:
        grouped_data = data.groupby(by=[primary_var, stacking_var]).size()\
                            .reset_index(name="Count")
        yaxis_label = "Number of Parking Sessions"
        
    mapping = {'month': 'Month', 'day_of_week': 'Day of the Week', 
               'hour': 'Hour', 'parking_zone': 'Parking Zone'}
    
    if primary_var == 'hour': 
        marker_colors = ["#6ed2b0", "#3abf91", "#2a8867", "#19513e"]

    elif primary_var == 'day_of_week':
        marker_colors = ["#e7d1a1", "#d9b568", "#ab832a", "#554115"]
        
    elif primary_var == 'ph_eve':
        marker_colors = ["#aea4e4", "#7d6dd3", "#4231a5", "#211852"]
    
    stack = data[stacking_var].unique()
    data = []
    for zone, color in zip(sorted(stack), marker_colors):
        data.append(go.Bar(name=zone, x=grouped_data[grouped_data[stacking_var] == zone][primary_var], 
                           y=grouped_data[grouped_data[stacking_var] == zone]['Count'], marker_color=color))
    fig = go.Figure(data=data)
    fig.update_layout(barmode='stack',
                      title="",
                      xaxis_title=mapping.get(primary_var),
                      yaxis_title=yaxis_label, 
                      xaxis_nticks=36)

    fig.show()
    # py.plot(fig, filename=primary_var + "_stacked_by_" + stacking_var, auto_open=True)    


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
#     py.plot(fig, filename=variable1 + "_by_" + variable2, auto_open=True)