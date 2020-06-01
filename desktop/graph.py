"""This module contains code used to graphically present data on the graph"""
import json

import plotly.graph_objects as go


class Graph:
    """
    Graph creating and displaying
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
    def add_y_axis_data(self, data_name, data, mode='lines+markers'):
        self.figure.add_trace(go.Scatter(x=self.x, y=data, mode=mode, name=data_name))

    def load_data_from_file(self, filename:str,x_entry:str, data:list, mode='lines+markers'):
        figures = []
        names = []
        for i in range(len(data)):
            figures.append([])
            names.append(data[i])
        with open(filename, "r") as file:
            for line in file:
                try:
                    result = json.loads(line)
                    self.x.append(result[x_entry])
                    for x in range(len(data)):
                        if result[data[x]]:
                            figures[x].append(result[data[x]])
                except ValueError or json.decoder.JSONDecodeError:
                    print("Could not read line: "+line)
                except KeyError as e:
                    print("Line: " + line+"Cannot find: " + str(e))
        for y in range(len(figures)):
            self.add_y_axis_data(names[y], figures[y], mode)

    def show(self):
        self.figure.show()
