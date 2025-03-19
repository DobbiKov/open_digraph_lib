from modules.open_digraph import *
import inspect

print("open_digraph:")
print(dir(open_digraph))
print(inspect.getsource(open_digraph.get_nodes_ids))
print(inspect.getdoc(open_digraph.get_nodes_ids))
print(inspect.getfile(open_digraph.get_nodes_ids))
print("node:")
print(dir(node))

# Sipan's test of visualize graph
n0 = node(0, 'x0', {}, {4:1})
n1 = node(1, 'x1', {}, {5:1} )
n2 = node(2, 'x2', {}, {3:1})
n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
n4 = node(4, '|', {0:0, 3:1}, {6:1})
n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
n6 = node(6, '|', {4:1, 5:1}, {9:1})
n7 = node(7, '&', {5:1, 3:1},{8:1})
n8 = node(8, '~', {7:1}, {9:1})
n9 = node(9, '&', {6:1, 8:1}, {})

graph_s = open_digraph(
    [0,1,2], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
)
graph_s.add_output_node(9)
# graph_s.display("graph_s")

# Another digraph example
m0 = node(0, 'a', {}, {2:1})
m1 = node(1, 'b', {}, {2:1})
m2 = node(2, '&', {0:1, 1:1}, {3:1, 8:1})
m3 = node(3, '~', {2:1}, {4:1, 9:1})
m4 = node(4, 'copy', {3:1}, {5:1, 6:1})
m5 = node(5, '|', {4:1}, {7:1, 10:1})
m6 = node(6, '|', {4:1}, {7:1})
m7 = node(7, '&', {5:1, 6:1}, {})
m01 = node(8, '01', {2:1}, {})
m02 = node(9, '02', {3:1}, {})
m03 = node(10, '03', {5:1}, {})

graph_g = open_digraph([0,1], [8, 9, 10], [m0, m1, m2, m3, m4, m5, m6, m7, m01, m02, m03])
# graph_g.add_output_node(7)
# graph_g.display("graph_g")



newg = graph_s.parallel(graph_g)

# print(newg.split())
newg.display("parallel")


new_c = graph_s.compose(graph_g)
# new_c.display("composition")



id4 = open_digraph.identity(4)
# id4.display("identity")


print(newg.connected_components())

i = 0
for k in newg.split():
    k.display(f"components_{i}")
    i+=1


# newg.icompose(graph_g)

# newg.display("compose")

# n0 = node(0, '0i', {3:1}, {1:1, 2:2})
# n1 = node(1, '1i', {0:1}, {3:3})
# n2 = node(2, '2o', {0:2}, {})
# n3 = node(3, '3a', {1:3, 4:1}, {0:1})
# n4 = node(4, '4i', {}, {3:1})
# graph = open_digraph([4], [2], 
#                   [n0, n1, n2, n3, n4])
#
# # graph = open_digraph.random(6, 9, 1, 2)
# graph.display()
#
# graph.save_as_dot_file("./dot.dot")
#
#
# graphNew = open_digraph.from_dot_file("./dot.dot")
# graphNew.display("from_file")
# print(graphNew.get_inputs_ids())
# print(graphNew.get_outputs_ids())
#
# graphNew.save_as_dot_file("./dotNew.dot")
#
# n0 = node(0, '0', {}, {1: 1})
# n1 = node(1, '', {0: 1}, {2: 1})
# n2 = node(2, '&', {1: 1}, {3: 1})
# n3 = node(3, '~', {2: 1}, {4: 1})
# n4 = node(4, '1', {3: 1}, {})
# valid_circ = open_digraph([0], [4], [n0, n1, n2, n3, n4])
# print(valid_circ.is_well_formed())
