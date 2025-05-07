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
    def test_add_some_nums(self):
        self.assertEqual(add_two_numbers(14, 27), 14 + 27)

        self.assertEqual(add_two_numbers(56, 12), 56 + 12)

if __name__ == "__main__":
    unittest.main()
