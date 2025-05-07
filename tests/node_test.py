import sys
import os

from modules.bool_circ import add_two_numbers, bool_circ
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.open_digraph_mixins.open_digraph_matrix_mixin import *
from modules.node import node

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {2:2}, {1:1})
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def test_get_parents(self):
        self.assertEqual(self.n0.get_parents(), {2:2})
    def test_get_children(self):
        self.assertEqual(self.n0.get_children(), {1:1})

    def test_set_id(self):
        self.n0.set_id(4)
        self.assertEqual(self.n0.get_id(), 4)

    def test_set_label(self):
        self.n0.set_label('b')
        self.assertEqual(self.n0.get_label(), 'b')
    def test_set_parents(self):
        self.n0.set_parents({3:3, 5:5})
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5})
    def test_set_children(self):
        self.n0.set_children({6:6, 2:2})
        self.assertEqual(self.n0.get_children(), {6:6, 2:2})

    def test_add_child_id(self):
        self.n0.set_children({6:6, 2:2})
        self.assertEqual(self.n0.get_children(), {6:6, 2:2})
        self.n0.add_child_id(4)
        self.assertEqual(self.n0.get_children(), {6:6, 2:2, 4:1})
        self.n0.add_child_id(4)
        self.assertEqual(self.n0.get_children(), {6:6, 2:2, 4:2})
    def test_add_parent_id(self):
        self.n0.set_parents({3:3, 5:5})
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5})
        self.n0.add_parent_id(4)
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5, 4:1})
        self.n0.add_parent_id(4)
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5, 4:2})
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)
    def test_remove_parent_children_one(self):
        n1 = node(0, 'a', {2:3, 3:1, 4:1}, {5:2, 6:1})
        self.assertEqual(n1.get_parents(), {2:3, 3:1, 4:1})
        self.assertEqual(n1.get_children(), {5:2, 6:1})

        n1.remove_parent_once(3)
        self.assertEqual(n1.get_parents(), {2:3, 4:1})

        n1.remove_parent_once(2)
        self.assertEqual(n1.get_parents(), {2:2, 4:1})

        n1.remove_child_once(5)
        self.assertEqual(n1.get_children(), {5:1, 6:1})

        n1.remove_child_once(6)
        self.assertEqual(n1.get_children(), {5:1})

    def test_remove_parent_children_id(self):
        n1 = node(0, 'a', {2:3, 3:1, 4:1}, {5:2, 6:1})
        self.assertEqual(n1.get_parents(), {2:3, 3:1, 4:1})
        self.assertEqual(n1.get_children(), {5:2, 6:1})

        n1.remove_parent_id(2)
        self.assertEqual(n1.get_parents(), {3:1, 4:1})
        n1.remove_parent_id(3)
        self.assertEqual(n1.get_parents(), {4:1})
        n1.remove_parent_id(5)
        self.assertEqual(n1.get_parents(), {4:1})
        n1.remove_parent_id(4)
        self.assertEqual(n1.get_parents(), {})

        n1.remove_child_id(10)
        self.assertEqual(n1.get_children(), {5:2, 6:1})
        n1.remove_child_id(5)
        self.assertEqual(n1.get_children(), {6:1})
        n1.remove_child_id(6)
        self.assertEqual(n1.get_children(), {})

if __name__ == "__main__":
    unittest.main()
