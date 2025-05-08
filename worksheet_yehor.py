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
# #
# # # num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() + '| num1 |' + str(idx) for idx in num_1_bc.get_inputs_ids()]
# # # num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() + '| num2 |' + str(idx) for idx in num_2_bc.get_inputs_ids()]
# #
# num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()]
# num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]
# #
# adder_1 = bool_circ.build_adder(2, num_1, num_2, '0')
# adder_1.display('adder_1')
# #
# adder_1.evaluate()
# adder_1.display('adder_1_evaluated')
#
# # print(get_result_of_evaluated_additioner(adder_1))
#
# print(add_two_numbers(14, 27))

# === transformation operations

# n0 = node(0, 'x1', {}, {1:1})
# n1 = node(1, '~',  {0:1}, {2:1})
# n2 = node(2, '~',   {1:1}, {3:1})
# n3 = node(3, 'out1',   {2:1}, {})
#
# graph = open_digraph([0], [3], [n0, n1, n2, n3])
# bc = bool_circ(graph)
# bc.display("temp")
# bc.transform_not_involution(2)
# bc.display("temp_transformated")

# transform_associative_xor

# enc_g = bool_circ.generate_4bit_encoder('0', '1', '0', '1')
# dec_g = bool_circ.generate_4bit_decoder('', '', '', '', '', '', '')
# comp = dec_g.compose(enc_g)
# comp = bool_circ(comp)
# comp.evaluate()
# print(get_result_of_evaluated_enc_dec(comp))
# ==== encoder
# enc_g = bool_circ.generate_4bit_encoder('0', '1', '0', '1')
# # enc_g.display("encoder")
# enc_g.evaluate()
# enc_g.display("encoder")
# print(get_result_of_evaluated_enc_dec(enc_g))
# dec_g = bool_circ.generate_4bit_decoder('0', '1', '0', '0', '1', '0', '1')
# dec_g = bool_circ.generate_4bit_decoder('', '', '', '', '', '', '')
# dec_g.display("dec")
# dec_g.evaluate()
# print(get_result_of_evaluated_enc_dec(dec_g))
# dec_g.display("decoder")
#
# comp = dec_g.compose(enc_g)
# comp = bool_circ(comp)
# comp.display("comp_enc")
# comp.evaluate()
# comp.display("evaluated")
# print(get_result_of_evaluated_enc_dec(comp))

# ==== carry look ahead
ca = bool_circ.carry_lookahead_4n(['0','0','1','1', '0', '0', '1', '1'], ['0','0','1','0', '0', '0', '1', '0'], '0')
ca.display("ca")
ca.evaluate()
print(get_result_of_evaluated_additioner(ca))
