import sys
import os

from modules.bool_circ import add_two_numbers, bool_circ
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.open_digraph_mixins.open_digraph_matrix_mixin import *
from modules.node import node
from modules.bool_circ import build_adder_0

class AddNumbersTest(unittest.TestCase):
    def test_evaluate_of_additioner(self):
        num_1_bc = bool_circ.from_number(2, 4)
        num_2_bc = bool_circ.from_number(3, 4)

        num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()]
        num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]

        adder_1 = bool_circ.build_adder(2, num_1, num_2, '0')

        output_num = len(adder_1.get_outputs_ids())
        max_depth = adder_1.get_graph_depth()

        self.assertEqual(output_num, 5)
        self.assertTrue(max_depth > 2)

        adder_1.evaluate()

        output_num = len(adder_1.get_outputs_ids())
        max_depth = adder_1.get_graph_depth()

        self.assertEqual(output_num, 5)
        self.assertEqual(max_depth, 2)

    def test_add_some_nums(self):
        self.assertEqual(add_two_numbers(14, 27), 14 + 27)

        self.assertEqual(add_two_numbers(56, 12), 56 + 12)

if __name__ == "__main__":
    unittest.main()
