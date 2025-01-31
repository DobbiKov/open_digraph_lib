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
    def test_getters(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])
        self.assertEqual(g0.get_nodes_ids(), [0, 1, 2, 3])
        self.assertEqual(g0.get_inputs_ids(), [0, 3])
        self.assertEqual(g0.get_outputs_ids(), [2])
        self.assertEqual(g0.get_nodes(), [n0, n1, n2, n3])
        self.assertEqual(g0.get_nodes_by_ids([1, 3]), [n1, n3])
        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3})

    def test_setters(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])
        self.assertEqual(g0.get_inputs_ids(), [0, 3])
        self.assertEqual(g0.get_outputs_ids(), [2])

        g0.add_input_id(4)
        self.assertEqual(g0.get_inputs_ids(), [0, 3, 4])

        g0.add_output_id(5)
        self.assertEqual(g0.get_outputs_ids(), [2, 5])

        g0.set_inputs([1,2])
        self.assertEqual(g0.get_inputs_ids(), [1,2])

        g0.set_outputs([3,4])
        self.assertEqual(g0.get_outputs_ids(), [3,4])
    def test_add_edge_no_id(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])

        self.assertEqual(n2.get_children(), {})
        g0.add_edge(2, 4)
        self.assertEqual(n2.get_children(), {})
        self.assertEqual(n2.get_parents(), {1:1})
        g0.add_edge(4, 2)
        self.assertEqual(n2.get_parents(), {1:1})

    def test_add_edge(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])

        self.assertEqual(n2.get_children(), {})
        self.assertEqual(n3.get_children(), {})
        self.assertEqual(n3.get_parents(), {})
        g0.add_edge(2, 3)
        self.assertEqual(n2.get_children(), {3:1})
        self.assertEqual(n3.get_parents(), {2:1})
    def test_add_empty_node(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])
        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3})
        new_id = g0.add_node('hey')
        self.assertEqual(new_id, 4)
        new_node = g0.get_nodes_by_ids([4])[0]
        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3, 4:new_node})
        self.assertEqual(new_node.get_label(), 'hey')
        self.assertEqual(new_node.get_id(), 4)
        self.assertEqual(new_node.get_parents(), {})
        self.assertEqual(new_node.get_children(), {})
    
    def test_well_formed_graph(self):
        n0 = node(0, 'input', {}, {1: 1})
        n1 = node(1, 'middle', {0: 1}, {2: 1})
        n2 = node(2, 'output', {1: 1}, {})
        g = open_digraph([0], [2], [n0, n1, n2])
        
        try:
            g.assert_is_well_formed()
        except AssertionError:
            self.fail("assert_is_well_formed() raised AssertionError unexpectedly!")

    def test_add_node(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {0:0}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])
        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3})
        self.assertEqual(g0.get_nodes_by_ids([0])[0].get_children(), {1:1})
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:3})
        self.assertEqual(g0.get_nodes_by_ids([2])[0].get_parents(), {1:1})
        new_id = g0.add_node('hey', {1:1, 0:1}, {2:2})
        self.assertEqual(g0.get_nodes_by_ids([0])[0].get_children(), {1:1, 4:1})
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:3, 4:1})
        self.assertEqual(g0.get_nodes_by_ids([2])[0].get_parents(), {1:1, 4:2})

        self.assertEqual(new_id, 4)
        self.assertEqual(g0.get_nodes_ids(), [0, 1, 2, 3, 4])

    def test_remove_edge(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {1:3}, {})
        g0 = open_digraph([0, 3], [2], 
                          [n0, n1, n2, n3])

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
