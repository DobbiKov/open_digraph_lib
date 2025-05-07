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

class TestBoolCircAdder(unittest.TestCase):
    def test_build_adder_0_basic_structure(self):
        reg1 = ['a']
        reg2 = ['b']
        carry = 'c'
        circ = build_adder_0(reg1, reg2, carry)

        # returns the right type
        self.assertIsInstance(circ, bool_circ)

        # must be acyclic and well-formed
        self.assertTrue(circ.is_acyclic(), "build_adder_0 yielded a cyclic graph")
        self.assertTrue(circ.is_well_formed(), "build_adder_0 yielded a malformed circuit")

        # 3 inputs (a, b, c) and 2 outputs (sum, carry‑out)
        self.assertEqual(len(circ.get_inputs_ids()), 3)
        self.assertEqual(len(circ.get_outputs_ids()), 2)

    def test_build_half_adder_alias(self):
        reg1 = ['x']
        reg2 = ['y']
        carry = '0'
        # build_adder(0, …) and build_half_adder(0, …) should coincide
        circ_from_adder = bool_circ.build_adder(0, reg1, reg2, carry)
        circ_half = bool_circ.build_half_adder(0, reg1, reg2)

        self.assertEqual(
            circ_from_adder.get_inputs_ids(), 
            circ_half.get_inputs_ids(),
            "Half‐adder inputs differ from build_adder(0, …)"
        )
        self.assertEqual(
            circ_from_adder.get_outputs_ids(),
            circ_half.get_outputs_ids(),
            "Half‐adder outputs differ from build_adder(0, …)"
        )

    def test_build_adder_dimensions_n1(self):
        # for 1‐bit adder: reg1/reg2 length = 2, inputs = 2·2+1 = 5, outputs = 2+1 = 3
        reg1 = ['u','v']
        reg2 = ['w','x']
        c = 'cin'
        circ = bool_circ.build_adder(1, reg1, reg2, c)

        self.assertTrue(circ.is_acyclic())
        self.assertTrue(circ.is_well_formed())

        self.assertEqual(len(circ.get_inputs_ids()), 5)
        self.assertEqual(len(circ.get_outputs_ids()), 3)

    def test_build_adder_dimensions_n2(self):
        # for 2‐bit adder: reg1/reg2 length = 4, inputs = 2·4+1 = 9, outputs = 4+1 = 5
        reg1 = ['a','b','c','d']
        reg2 = ['e','f','g','h']
        c = 'cin'
        circ = bool_circ.build_adder(2, reg1, reg2, c)

        self.assertTrue(circ.is_acyclic())
        self.assertTrue(circ.is_well_formed())

        self.assertEqual(len(circ.get_inputs_ids()), 9)
        self.assertEqual(len(circ.get_outputs_ids()), 5)

    def test_build_adder_invalid_arguments(self):
        # negative n
        with self.assertRaises(AssertionError):
            bool_circ.build_adder(-1, ['a'], ['b'], 'c')

        # mismatched register lengths
        with self.assertRaises(AssertionError):
            bool_circ.build_adder(1, ['x'], ['y','z'], 'c')

if __name__ == "__main__":
    unittest.main()
