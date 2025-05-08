from modules.graphs import graph_de_prof_td_10
from modules.open_digraph import *
from modules.bool_circ import *
import inspect
from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")

# === ()
# g_from_par = parse_parentheses("(((0)&(0))|(0))")
# g_from_par = parse_parentheses("(((x0)&(x1))|(x2))")
# g_from_par[0].display("pars")

# === test evaluate adder
# num_1_bc = bool_circ.from_number(2, 4)
# num_2_bc = bool_circ.from_number(3, 4)
#
# # num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() + '| num1 |' + str(idx) for idx in num_1_bc.get_inputs_ids()]
# # num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() + '| num2 |' + str(idx) for idx in num_2_bc.get_inputs_ids()]
#
# num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()]
# num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]
#
# adder_1 = bool_circ.build_adder(2, num_1, num_2, '0')
# # adder_1.display('adder_1')
#
# adder_1.evaluate()
# # adder_1.display('adder_1_evaluated')
#
# # print(get_result_of_evaluated_additioner(adder_1))
#
# print(add_two_numbers(14, 27))

# === transformation operations

n0 = node(0, 'x1', {}, {3: 1})
n1 = node(1, 'x2', {}, {3: 1})
n2 = node(2, 'x3', {}, {4: 1})
n3 = node(3, '^', {0:1, 1:1, 4:2}, {5: 1})
n4 = node(4, '', {2:1}, {3:2, 6:1, 7:1})
n5 = node(5, 'out1', {3:1}, {})
n6 = node(6, 'out2', {4:1}, {})
n7 = node(7, 'out3', {4:1}, {})

graph = open_digraph([0, 1, 2], [5, 6, 7], [n0, n1, n2, n3, n4, n5, n6, n7])
bc = bool_circ(graph)
bc.display("temp")
bc.transform_involution_xor(3)
bc.display("temp_transformated")

# transform_associative_xor
