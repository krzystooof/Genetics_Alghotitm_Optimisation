"""This module contains code used to graphically present data on the graph"""
import plotly.graph_objects as go


class Graph:
    """
    Graph creating and showing
    @author: Krzysztof Greczka
    """

    def __init__(self, title="Graph", x_axis_title="x_axis", y_axis_title="y_axis", additonal_x_info=[]):
        self.title = title
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title
        self.figure = go.Figure()
        self.x = []
        for i in range(len(additonal_x_info)):
            self.x.append(str(i + 1) + "[" + str(additonal_x_info[i]) + "]")

    # mode = ['lines','lines+markers', 'markers']
    def add_y_axis_data(self, data_name, data, mode):
        self.figure.add_trace(go.Scatter(x=self.x, y=data, mode=mode, name=data_name))

    def show(self):
        self.figure.show()
