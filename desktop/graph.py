"""This module contains code used to graphically present data on the graph"""
import plotly.graph_objects as go


class Graph:
    """
    Graph creating and showing
    @author: Krzysztof Greczka
    """

    def __init__(self, title="Graph", x_axis_title="x_axis", y_axis_title="y_axis", x_data=[""]):
        self.title = title
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title
        self.figure = go.Figure()

    # mode = ['lines','lines+markers', 'markers']
    def add_y_axis_data(self, data_name,additonal_x_info, data, mode):
        x = []
        for i in range(1, len(data)):
            x.append(str(i)+"["+str(additonal_x_info[i])+" values]")

        self.figure.add_trace(go.Scatter(x=x, y=data, mode=mode, name=data_name))

    def show(self):
        self.figure.show()
