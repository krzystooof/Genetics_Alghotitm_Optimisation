from desktop.graph import Graph


filename = 'time(discard).txt).txt'

my_graph = Graph()
my_graph.load_data_from_file(filename, 'value', ['time', 'accuracy', 'generation'])
my_graph.show()
