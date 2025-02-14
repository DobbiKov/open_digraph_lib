from modules.open_digraph import *
from modules.viz import *
import inspect

print("open_digraph:")
print(dir(open_digraph))
print(inspect.getsource(open_digraph.get_nodes_ids))
print(inspect.getdoc(open_digraph.get_nodes_ids))
print(inspect.getfile(open_digraph.get_nodes_ids))
print("node:")
print(dir(node))

# Sipan's test of visualize graph
# n0 = node(0, 'x0', {}, {4:4})
# n1 = node(1, 'x1', {}, {5:5} )
# n2 = node(2, 'x2', {}, {3:3})
# n3 = node(3, 'copy', {2:2}, {4:4, 7:7})
# n4 = node(4, '|', {0:0, 3:3}, {6:6})
# n5 = node(5, 'copy', {1:1}, {6:6, 7:7})
# n6 = node(6, '|', {4:4, 5:5}, {9:9})
# n7 = node(7, '&', {5:5, 3:3},{8:8})
# n8 = node(8, '~', {7:7}, {9:9})
# n9 = node(9, '&', {6:6, 8:8}, {})
#
# graph = open_digraph(
#     [0,1,2], [9], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
# )

n0 = node(0, '0i', {3:1}, {1:1, 2:2})
n1 = node(1, '1i', {0:1}, {3:3})
n2 = node(2, '2o', {0:2}, {})
n3 = node(3, '3a', {1:3, 4:1}, {0:1})
n4 = node(4, '4i', {}, {3:1})
graph = open_digraph([4], [2], 
                  [n0, n1, n2, n3, n4])

#
graph = open_digraph.random(6, 9, 1, 2)
# dot = vizualize_graph(graph)
#
# dot.render('graph', view=True)

graph.save_as_dot_file("./dot.dot")
