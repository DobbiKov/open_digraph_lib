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

# circ = bool_circ.random_bool_circ_from_graph(graph_de_prof_td_10(), 1, 3)
# circ.display("circ")

# circ_add_0 = bool_circ.build_adder(3, ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'], ['x0\'', 'x1\'', 'x2\'', 'x3\'', 'x4\'', 'x5\'', 'x6\'', 'x7\''], 'c')
# print(circ_add_0)
# circ_add_0.display("circ_add_0")

# from_num_c = bool_circ.from_number(11)
# from_num_c.display("from_num")


# encoder
# temp_test_graph = bool_circ.generate_4bit_decoder("x0", "x1", "x2", "x3", "x4", "x5", "x6")
# temp_test_graph.display("decoder", verbose=False)
# print(temp_test_graph.get_outputs_ids()) # correct order of output nodes

# circ, vars = parse_parentheses("((x0)&((x1)|(x2)))|((x1)&(~(x2)))", "(x1)&(x2)")
# circ, vars = parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
#
# circ.display("circ", verbose=True)
# # res = graph_s.sort_topologicly()
# print(vars)


# === test carry look ahead 
ca = bool_circ.carry_lookahead_4n(['a1','a2','a3','a4', 'a5', 'a6', 'a7', 'a8'], ['b1','b2','b3','b4', 'b5', 'b6', 'b7', 'b8'], 'c0')

ca = bool_circ.carry_lookahead_4(['a1','a2','a3','a4'], ['b1','b2','b3','b4'], 'c0')

# ca.display("ca", verbose=False)
ca = bool_circ.carry_lookahead_4n(['a1','a2','a3','a4'], ['b1','b2','b3','b4'], 'c0')
# ca.display("ca", verbose=False)

ca = bool_circ.carry_lookahead_4(['0','0','1','0'], ['0','0','1','1'], '0')
# ca.display("ca", verbose=False)
ca.evaluate()
# ca.display("ca_eval", verbose=False)
# === ()
# g_from_par = parse_parentheses("(((0)&(0))|(0))")
# g_from_par = parse_parentheses("(((x0)&(x1))|(x2))")
# g_from_par[0].display("pars")

# === test evaluate adder
num_1_bc = bool_circ.from_number(2, 4)
num_2_bc = bool_circ.from_number(3, 4)

# num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() + '| num1 |' + str(idx) for idx in num_1_bc.get_inputs_ids()]
# num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() + '| num2 |' + str(idx) for idx in num_2_bc.get_inputs_ids()]

num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()]
num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]

vars1 = [f'x{i}' for i in range(len(num_1))]
vars2 = [f'y{i}' for i in range(len(num_2))]

var_to_num = {}
for i in range(len(vars1)):
    var_to_num[vars1[i]] = num_1[i]

for i in range(len(vars2)):
    var_to_num[vars2[i]] = num_2[i]

print(num_1)
print(num_2)


adder_1 = bool_circ.build_adder(2, vars1, vars2, '0')
for node_id in adder_1.get_inputs_ids():
    if adder_1[node_id].label in ("0", "1"):
        continue
    adder_1[node_id].label = var_to_num[ adder_1[node_id].label ]


adder_1 = bool_circ.build_adder(2, num_1, num_2, '0')
adder_1.display('adder_1')

adder_1.evaluate()
adder_1.display('adder_1_evaluated')

output_nodes = [ n for n in adder_1.get_nodes_by_ids(adder_1.get_outputs_ids())]
par_out_nodes = [ adder_1.get_id_node_map()[ list(n.get_parents().keys())[0] ] for n in output_nodes]

labels_for_par_nodes = [n.get_label() for n in par_out_nodes]

print(labels_for_par_nodes[1:])

# print([ n.get_label() for n in adder_1.get_nodes_by_ids(adder_1.get_outputs_ids())])


