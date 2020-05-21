import plotly.graph_objects as go


class Graph:
    def __init__(self, title="Graph", x_axis_title="x_axis", y_axis_title="y_axis", x_data=[""]):
        self.title = title
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title
        self.x_axis_data = x_data
        self.figure = go.Figure()

    # mode = ['lines','lines+markers', 'markers']
    def add_y_axis_data(self, data_name, data, mode):
        self.figure.add_trace(go.Scatter(x=self.x_axis_data, y=data, mode=mode, name=data_name))

    def show(self):
        self.figure.show()


if __name__ == '__main__':
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
    graph = Graph("Graph", "x", "y", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    graph.add_y_axis_data("high_2000", [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3],
                          'lines+markers')
    graph.add_y_axis_data("low_2000", [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9, 17, 20],
                          'lines+markers')
    graph.show()
