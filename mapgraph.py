# Laron Lemon, Student ID: #000927228

# import library
import csv


# create node object(s)
class Node:
    def __init__(self, name, address):
        self.name = name
        self.address = address


# create graph objects(s)
class Graph:
    def __init__(self):
        self.adjacent_nodes = {}
        self.edge_weights = {}
        self.distance = 1.0
        self.node_address = []

    def add_node(self, new_node):
        self.adjacent_nodes[new_node] = []

    def add_directed_edge(self, from_node, to_node, weight=1.0):
        self.edge_weights[(from_node, to_node)] = weight
        self.adjacent_nodes[from_node].append(to_node)

    def add_undirected_edge(self, node_a, node_b, weight=1.0):
        self.add_directed_edge(node_a, node_b, weight)
        self.add_directed_edge(node_b, node_a, weight)

# load map data from csv
    @staticmethod
    def map_data(csv_file, graph):
        nodes = []
        edges = []
        with open(csv_file) as map_table:
            read_map_table = csv.reader(map_table)
            next(read_map_table, None)
            for row in read_map_table:
                location = Node(row[0], row[1])
                street_zip = location.address.split("\n")
                graph.node_address.append((location.name, street_zip))
                graph.add_node(location.name)
                nodes.append(location.name)
                edges.append(row[2:])

            for index, item in enumerate(edges):
                node_index = 0
                distance_index = 0
                while node_index < index:
                    node_a = nodes[index]
                    node_b = nodes[node_index]
                    distance = item[distance_index]
                    node_index += 1
                    distance_index += 1
                    graph.add_undirected_edge(node_a, node_b, distance)

