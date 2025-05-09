from modules.graphs import graph_de_prof_td_10
from modules.open_digraph import *
from modules.bool_circ import *
import inspect
from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")


num_1_bc = bool_circ.from_number(2, 4)
num_2_bc = bool_circ.from_number(3, 4)

num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()]
num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]

adder_1 = bool_circ.build_half_adder(2, num_1, num_2)
adder_1.display('half_adder_1', verbose=True)

adder_1.evaluate()
# adder_1.evaluate()
# adder_1.display('adder_1_evaluated')
