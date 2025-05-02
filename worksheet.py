from modules.graphs import graph_de_prof_td_10
from modules.open_digraph import *
from modules.bool_circ import *
import inspect
from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")

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
    [], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
)
# graph_s.add_output_node(9)
# graph_s.display("graph_s", verbose=False)

# res = graph_s.longest_path(1, 9)
# print(res)



# rand_g = open_digraph.random(6, 1, form="DAG")
# rand_g.display("rand_g")

# circ = bool_circ.random_bool_circ_from_graph(graph_de_prof_td_10(), 1, 3)
# circ.display("circ")

# circ_add_0 = build_adder(2, ['x0', 'x1', 'x2', 'x3'], ['x0\'', 'x1\'', 'x2\'', 'x3\''], 'c')
# print(circ_add_0)
# circ_add_0.display("circ_add_0")

from_num_c = bool_circ.from_number(11)
# from_num_c.display("from_num")

# circ, vars = parse_parentheses("((x0)&((x1)|(x2)))|((x1)&(~(x2)))", "(x1)&(x2)")
# circ, vars = parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
#
# circ.display("circ", verbose=True)
# # res = graph_s.sort_topologicly()
# print(vars)


# 
# ca = bool_circ.carry_lookahead_4n(['a1','a2','a3','a4', 'a5', 'a6', 'a7', 'a8'], ['b1','b2','b3','b4', 'b5', 'b6', 'b7', 'b8'], 'c0')

ca = bool_circ.carry_lookahead_4n(['a1','a2','a3','a4'], ['b1','b2','b3','b4'], 'c0')
ca.display("ca", verbose=False)

# open_digraph.identity(4).display("identity", verbose=False)