import sys
import os
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)
    def test_init_opendigraph(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {1:1}, {2:2})
        n2 = node(2, 'o', {2:2}, {})
        g0 = open_digraph([0], [2], 
                          [n0, n1, n2])

        self.assertEqual(g0.inputs, [0])
        self.assertEqual(g0.outputs, [2])
        self.assertEqual(g0.nodes, {0:n0, 1:n1, 2:n2})

        for id in g0.inputs:
            self.assertEqual(g0.nodes[id].parents, {})
        for id in g0.outputs:
            self.assertEqual(g0.nodes[id].children, {})
    def test_copy(self):
        g = open_digraph.empty()
        self.assertIsNot(g.copy(), g)
    def test_new_id_plus_one(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {1:1}, {2:2})
        n2 = node(2, 'o', {2:2}, {})
        g0 = open_digraph([0], [2], 
                          [n0, n1, n2])
        self.assertEqual(g0.new_id(), 3)

    def test_new_id_middle(self):

        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(3, 'o', {1:1}, {})
        g0 = open_digraph([0], [2], 
                          [n0, n1, n2])
        self.assertEqual(g0.new_id(), 2)


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
        self.assertEqual(self.n0.get_children(), {6:6, 2:2, 4:4})
    def test_add_parent_id(self):
        self.n0.set_parents({3:3, 5:5})
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5})
        self.n0.add_parent_id(4)
        self.assertEqual(self.n0.get_parents(), {3:3, 5:5, 4:4})
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)

if __name__ == "__main__":
    unittest.main()
