from modules.open_digraph import *
import inspect

print("open_digraph:")
print(dir(open_digraph))
print(inspect.getsource(open_digraph.get_nodes_ids))
print(inspect.getdoc(open_digraph.get_nodes_ids))
print(inspect.getfile(open_digraph.get_nodes_ids))
print("node:")
print(dir(node))

# Sipan's test for visualizing graphs
n0 = node(0, 'x0', {}, {4:1})
n1 = node(1, 'x1', {}, {5:1} )
n2 = node(2, 'x2', {}, {3:1})
n3 = node(3, 'copy 1', {2:1}, {4:1, 7:1})
n4 = node(4, '| 1', {0:0, 3:1}, {6:1})
n5 = node(5, 'copy 2', {1:1}, {6:1, 7:1})
n6 = node(6, '| 2', {4:1, 5:1}, {9:1})
n7 = node(7, '& 1', {5:1, 3:1},{8:1})
n8 = node(8, '~', {7:1}, {9:1})
n9 = node(9, '& 2', {6:1, 8:1}, {})

graph_s = open_digraph(
    [0,1,2], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
)
graph_s.add_output_node(9)
graph_s.display("graph_s")

res = graph_s.common_ancestors(6, 8)
print(res)
for key in res.keys():
    label = graph_s.get_id_node_map()[key].get_label()
    print(f"{label}: {res[key]}")

