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

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)

if __name__ == "__main__":
    unittest.main()
