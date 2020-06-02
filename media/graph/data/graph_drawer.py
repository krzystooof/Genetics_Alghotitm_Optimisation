"""Tool for drawing graphs"""
from desktop.graph import Graph

#  Here type \/\/\/ file containing data 
filename = 'time(discard).txt'

my_graph = Graph()
my_graph.load_data_from_file(filename, 'value', ['time', 'accuracy', 'generation'])
my_graph.show()
