import sys
import os

from modules.bool_circ import bool_circ
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
        self.assertRaises(AssertionError, g0.assert_is_well_formed)
    
    def test_well_formed_graph(self):
        n0 = node(0, 'input', {}, {1: 1})
        n1 = node(1, 'middle', {0: 1}, {2: 1})
        n2 = node(2, 'output', {1: 1}, {})
        g = open_digraph([0], [2], [n0, n1, n2])
        
        g.assert_is_well_formed()

        n2 = node(2, 'output', {}, {3: 1})
        g = open_digraph([0], [2], [n0, n1, n2])
        self.assertRaises(AssertionError, g.assert_is_well_formed)

        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])

        g0.assert_is_well_formed()

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

        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3})
        self.assertEqual(g0.get_nodes_by_ids([0])[0].get_children(), {1:1, 2:1})
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:3})
        self.assertEqual(g0.get_nodes_by_ids([2])[0].get_parents(), {1:1})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {1:3})
        g0.remove_edge(3, 1)
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:3})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {1:3})

        g0.remove_edge(1, 3)
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:2})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {1:2})

        g0.remove_parallel_edges(1, 3)
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {})

    def test_remove_node_by_id(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {1:1}, {})
        n3 = node(3, 'a', {1:3}, {})
        g0 = open_digraph([0, 3], [2, 1], 
                          [n0, n1, n2, n3])
        self.assertEqual(g0.get_outputs_ids(), [2, 1])
        self.assertEqual(g0.get_id_node_map(), {0:n0, 1:n1, 2:n2, 3:n3})
        self.assertEqual(g0.get_nodes_by_ids([0])[0].get_children(), {1:1, 2:1})
        self.assertEqual(g0.get_nodes_by_ids([1])[0].get_children(), {3:3})
        self.assertEqual(g0.get_nodes_by_ids([2])[0].get_parents(), {1:1})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {1:3})
        self.assertEqual(g0.get_nodes_ids(), [0, 1, 2, 3])

        g0.remove_node_by_id(1)
        self.assertEqual(g0.get_nodes_ids(), [0, 2, 3])
        self.assertEqual(g0.get_nodes_by_ids([0])[0].get_children(), {2:1})
        self.assertEqual(g0.get_nodes_by_ids([3])[0].get_parents(), {})
        self.assertEqual(g0.get_outputs_ids(), [2])

    def test_add_input_node(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])
        g0.assert_is_well_formed()
        self.assertEqual(g0.get_inputs_ids(), [4])

        self.assertEqual(g0.get_id_node_map()[0].get_parents(), {})
        self.assertIsNot(5 in g0.get_nodes_ids(), True)
        g0.add_input_node(0)
        self.assertEqual(g0.get_id_node_map()[0].get_parents(), {5:1})
        self.assertIs(5 in g0.get_nodes_ids(), True)
        self.assertEqual(g0.get_id_node_map()[5].get_children(), {0:1})
        self.assertEqual(g0.get_inputs_ids(), [4, 5])
        g0.assert_is_well_formed()

    def test_add_output_node(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])
        g0.assert_is_well_formed()
        self.assertEqual(g0.get_nodes_ids(), [0, 1, 2, 3, 4])
        self.assertEqual(g0.get_outputs_ids(), [2])
        self.assertEqual(g0.get_id_node_map()[3].get_children(), {})

        g0.add_output_node(3)
        self.assertEqual(g0.get_nodes_ids(), [0, 1, 2, 3, 4, 5])
        self.assertEqual(g0.get_outputs_ids(), [2, 5])
        self.assertEqual(g0.get_id_node_map()[3].get_children(), {5:1})
        self.assertEqual(g0.get_id_node_map()[5].get_parents(), {3:1})
        g0.assert_is_well_formed()

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

class TestOpenDigraphWellFromedNess(unittest.TestCase):
    def setUp(self):
        """
        Set up a simple well-formed graph for testing:
        
        input_node (id=1) -> A (id=2) -> output_node (id=3)
        """
        self.input_node = node(identity=1, label='input', parents={}, children={2:1})
        self.node_A = node(identity=2, label='A', parents={1:1}, children={3:1})
        self.output_node = node(identity=3, label='output', parents={2:1}, children={})
        
        self.good_graph = open_digraph(
            inputs=[1],
            outputs=[3],
            nodes=[self.input_node, self.node_A, self.output_node]
        )
        self.good_graph.assert_is_well_formed()

    def test_well_formed_accepts_good_graphs(self):
        """
        Test that a well-formed graph passes the well-formedness check.
        """
        try:
            self.good_graph.assert_is_well_formed()
        except AssertionError as e:
            self.fail(f"Well-formed graph was incorrectly rejected: {e}")

    def test_well_formed_rejects_bad_graphs(self):
        """
        Test that malformed graphs are correctly identified and rejected.
        """
        # Case 1: Input node has a parent
        bad_input_node = node(identity=1, label='input', parents={2:1}, children={2:1})
        bad_graph1 = open_digraph(
            inputs=[1],
            outputs=[3],
            nodes=[bad_input_node, self.node_A, self.output_node]
        )
        with self.assertRaises(AssertionError):
            bad_graph1.assert_is_well_formed()
        
        # Case 2: Node with inconsistent multiplicity
        bad_node_A = node(identity=2, label='A', parents={1:2}, children={3:1})  # Multiplicity 2 from input
        bad_graph2 = open_digraph(
            inputs=[1],
            outputs=[3],
            nodes=[self.input_node, bad_node_A, self.output_node]
        )
        with self.assertRaises(AssertionError):
            bad_graph2.assert_is_well_formed()
        
        # Case 3: Output node has multiple parents
        bad_output_node = node(identity=3, label='output', parents={2:1, 4:1}, children={})
        bad_graph3 = open_digraph(
            inputs=[1],
            outputs=[3],
            nodes=[self.input_node, self.node_A, bad_output_node]
        )
        with self.assertRaises(AssertionError):
            bad_graph3.assert_is_well_formed()

    def test_add_remove_node_preserves_well_formedness(self):
        """
        Test that adding and removing nodes maintains the graph's well-formedness.
        """
        graph = self.good_graph.copy()
        graph.assert_is_well_formed()
        
        # Add a new node B (id=4) connected from A to output
        new_id = graph.add_node()
        graph.add_edge(new_id, 2)
        
        # Update outputs to include node B's child if necessary
        # In this case, output node remains the same
        graph.assert_is_well_formed()
        
        # Remove node B
        graph.remove_node_by_id(4)
        graph.assert_is_well_formed()

    def test_add_remove_edge_preserves_well_formedness(self):
        """
        Test that adding and removing edges (excluding those involving input/output nodes) maintains well-formedness.
        """
        graph = self.good_graph.copy()
        graph.assert_is_well_formed()
        
        # Add a loop edge on node A (id=2)
        graph.add_edge(2, 2)
        graph.assert_is_well_formed()
        
        # Remove the loop edge
        graph.remove_edge(2, 2)
        graph.assert_is_well_formed()
        
        # Add an edge from A to a new node (id=4) and ensure it's handled correctly
        new_id = graph.add_node('')
        graph.add_edge(new_id, 2)
        graph.assert_is_well_formed()
        
        # Remove the edge from A to C
        graph.remove_edge(2, 4)
        graph.assert_is_well_formed()

    def test_add_input_output_preserves_well_formedness(self):
        """
        Test that adding input and output nodes via provided methods maintains the graph's well-formedness.
        """
        graph = open_digraph.empty()
        
        # Add primary nodes A (id=1) and B (id=2)
        node_A = node(identity=1, label='A', parents={}, children={2:1})
        node_B = node(identity=2, label='B', parents={1:1}, children={})
        graph.nodes = {1: node_A, 2: node_B}
        
        # Add edge A -> B
        graph.add_edge(1, 2)
        
        # Add input node pointing to A
        input_id = graph.add_input_node(1)
        self.assertNotEqual(input_id, -1, "Failed to add input node.")
        graph.assert_is_well_formed()
        
        # Add output node pointing from B
        output_id = graph.add_output_node(2)
        self.assertNotEqual(output_id, -1, "Failed to add output node.")
        graph.assert_is_well_formed()
        
        # Remove input node
        graph.remove_node_by_id(input_id)
        graph.assert_is_well_formed()
        
        # Remove output node
        graph.remove_node_by_id(output_id)
        graph.assert_is_well_formed()

    def test_remove_nonexistent_node(self):
        """
        Test that removing a non-existent node does not affect the graph's well-formedness.
        """
        graph = self.good_graph.copy()
        graph.assert_is_well_formed()
        
        # Attempt to remove a node that doesn't exist
        graph.remove_node_by_id(999)  # Assuming 999 is not a valid node ID
        graph.assert_is_well_formed()

    def test_add_edge_with_nonexistent_nodes(self):
        """
        Test that adding an edge involving non-existent nodes does not alter the graph.
        """
        graph = self.good_graph.copy()
        graph.assert_is_well_formed()
        
        # Attempt to add an edge where source node does not exist
        result = graph.add_edge(999, 2)
        self.assertFalse(result, "Adding edge with nonexistent source should return False.")

        graph.assert_is_well_formed()
        
        # Attempt to add an edge where target node does not exist
        result = graph.add_edge(2, 999)
        self.assertFalse(result, "Adding edge with nonexistent target should return False.")
        graph.assert_is_well_formed()

    def test_add_duplicate_input_output(self):
        """
        Test that adding duplicate input or output nodes is handled correctly.
        """
        graph = self.good_graph.copy()
        graph.assert_is_well_formed()
        
        # Attempt to add the same input node again
        duplicate_input_id = graph.add_input_node(1)  # Assuming node 1 exists
        self.assertEqual(duplicate_input_id, -1, "Adding duplicate input node should return -1.")
        graph.assert_is_well_formed()
        
        # Attempt to add the same output node again
        duplicate_output_id = graph.add_output_node(3)  # Assuming node 3 exists
        self.assertEqual(duplicate_output_id, -1, "Adding duplicate output node should return -1.")
        graph.assert_is_well_formed()

    def test_copy_graph(self):
        """
        Test that copying a graph results in an identical but separate graph.
        """
        graph_copy = self.good_graph.copy()
        graph_copy.assert_is_well_formed()
        self.good_graph.assert_is_well_formed()
        for i in self.good_graph.get_nodes_ids():
            self.assertNotEqual(self.good_graph.get_id_node_map()[i], graph_copy.get_id_node_map()[i])
        
        # Modify the copy
        new_id = graph_copy.add_node(label='B', parents={2:1}, children={3:1})
        self.assertRaises(AssertionError, graph_copy.assert_is_well_formed)
        
        # Ensure original graph remains unchanged
        self.assertNotIn(new_id, self.good_graph.get_nodes_ids(), "Original graph should not contain the new node added to the copy.")
        self.assertNotEqual(graph_copy, self.good_graph)
        self.good_graph.assert_is_well_formed()

class TestGraphWithMatrix(unittest.TestCase):
    def test_random_int_matrix(self):
        for i in range(10):
            mat = random_int_matrix(10, 10)
            for row_idx, row in enumerate(mat):
                for col_idx, e in enumerate(row):
                    self.assertTrue(e >= 0 and e < 10)
                    if row_idx == col_idx:
                        self.assertEqual(e, 0)

    def test_random_symetric_int_matrix2(self):
        for i in range(10):
            mat = random_symetric_int_matrix(10, 10)
            for row_idx, row in enumerate(mat):
                for col_idx, e in enumerate(row):
                    self.assertEqual(mat[row_idx][col_idx], mat[col_idx][row_idx])
                for e in mat[row_idx]:
                    self.assertTrue(e >= 0 and e < 10)


    def test_random_oriented_int_matrix(self):
        for i in range(10):
            mat = random_oriented_int_matrix(10, 10)
            for row_idx, row in enumerate(mat):
                for col_idx, e in enumerate(row):
                    self.assertTrue(e >= 0 and e < 10)
                    if row_idx == col_idx:
                        self.assertEqual(e, 0)
                    if e != 0:
                        self.assertEqual(mat[col_idx][row_idx], 0)

    def test_random_triangular_int_matrix(self):
        for i in range(10):
            mat = random_triangular_int_matrix(10, 10)
            for row_idx, row in enumerate(mat):
                for col_idx, e in enumerate(row):
                    self.assertTrue(e >= 0 and e < 10)
                    if row_idx == col_idx:
                        self.assertEqual(e, 0)
                    if row_idx > col_idx:
                        self.assertEqual(e, 0)

    def test_graph_from_adjacency_matrix(self):
        mat = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]
        g = graph_from_adjacency_matrix(mat)
        g.assert_is_well_formed()

    def test_graph_from_empty_adjacency_matrix(self):
        mat = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        g = graph_from_adjacency_matrix(mat)
        g.assert_is_well_formed()
    
    def test_random_symetric_int_matrix(self):
        for i in range(10):
            mat = random_symetric_int_matrix(10, 10)
            for i in range(10):
                for j in range(10):
                    self.assertEqual(mat[i][j], mat[j][i])
                for e in mat[i]:
                    self.assertTrue(e >= 0 and e < 10)

    def test_well_formed_from_random_matrix(self):
        mat = random_int_matrix(5, 9)
        g = graph_from_adjacency_matrix(mat)
        g.assert_is_well_formed()

    def test_random_graph(self):
        g = open_digraph.random(5, 9, 1, 0, "free")
        g.assert_is_well_formed()

        g = open_digraph.random(5, 9, 3, 2, "free")
        g.assert_is_well_formed()

    def test_graph_to_adjecancy_matrix(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([], [], 
                          [n0, n1, n2, n3, n4])
        mat = g0.adjacancy_matrix()
        self.assertEqual(mat[0][1], 1)
        self.assertEqual(mat[0][2], 1)
        self.assertEqual(mat[1][3], 3)
        self.assertEqual(mat[4][3], 1)

        self.assertEqual(mat[4][2], 0)
        self.assertEqual(mat[4][4], 0)
        self.assertEqual(mat[4][1], 0)
        self.assertEqual(mat[0][3], 0)
        self.assertEqual(mat[0][4], 0)
        self.assertEqual(mat[1][4], 0)
        self.assertEqual(mat[1][2], 0)
        self.assertEqual(mat[1][1], 0)
        self.assertEqual(mat[1][0], 0)
        for i in range(2, 4):
            for j in range(5):
                self.assertEqual(mat[i][j], 0)

    def test_graph_to_adjecancy_matrix_with_io(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])
        mat = g0.adjacancy_matrix()
        self.assertEqual(mat[0][1], 1)
        self.assertEqual(mat[0][0], 0)
        self.assertEqual(mat[0][2], 0)

        self.assertEqual(mat[1][2], 3)
        self.assertEqual(mat[1][1], 0)
        self.assertEqual(mat[1][0], 0)

        self.assertEqual(mat[2][2], 0)
        self.assertEqual(mat[2][1], 0)
        self.assertEqual(mat[2][0], 0)

    def test_get_node_id_to_enumerate_mapping(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([], [], 
                          [n0, n1, n2, n3, n4])
        mapping = g0.get_node_id_to_enumerate_mapping()
        for node_id in g0.get_nodes_ids():
            self.assertEqual(node_id in mapping.keys(), True)
        self.assertEqual(len(mapping.keys()), len(g0.get_nodes()))

        new_id = g0.add_input_node(3)

        mapping = g0.get_node_id_to_enumerate_mapping()
        self.assertEqual(len(mapping.keys()), len(g0.get_nodes()))
        self.assertEqual(new_id in mapping.keys(), True)

        mapping = g0.get_node_id_to_enumerate_mapping(True, False)
        self.assertNotEqual(len(mapping.keys()), len(g0.get_nodes()))
        self.assertFalse(new_id in mapping.keys())

    def test_get_node_id_to_enumerate_mapping2(self):
        n0 = node(0, 'i', {}, {1:1, 2:1})
        n1 = node(1, 'i', {0:1}, {3:3})
        n2 = node(2, 'o', {0:1}, {})
        n3 = node(3, 'a', {1:3, 4:1}, {})
        n4 = node(4, 'i', {}, {3:1})
        g0 = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])
        mapping = g0.get_node_id_to_enumerate_mapping()
        for node_id in g0.get_nodes_ids():
            self.assertEqual(node_id in mapping.keys(), True)
        self.assertEqual(len(mapping.keys()), len(g0.get_nodes()))

        self.assertEqual(4 in mapping.keys(), True)

        mapping_without_inputs = g0.get_node_id_to_enumerate_mapping(True, False)
        self.assertNotEqual(len(mapping_without_inputs.keys()), len(g0.get_nodes()))
        self.assertEqual(4 in mapping_without_inputs.keys(), False)

        mapping_without_outputs = g0.get_node_id_to_enumerate_mapping(False, True)
        self.assertNotEqual(len(mapping_without_outputs.keys()), len(g0.get_nodes()))
        self.assertEqual(4 in mapping_without_outputs.keys(), True)
        self.assertEqual(2 in mapping_without_outputs.keys(), False)

    def test_shidft_indices(self):
        n0 = node(0, '0i', {3:1}, {1:1, 2:2})
        n1 = node(1, '1i', {0:1}, {3:3})
        n2 = node(2, '2o', {0:2}, {})
        n3 = node(3, '3a', {1:3, 4:1}, {0:1})
        n4 = node(4, '4i', {}, {3:1})
        graph = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])

        graph.shift_indices(5)

        # change of inputs, outputs, node ids
        self.assertEqual(graph.get_inputs_ids(), [9])
        self.assertEqual(graph.get_outputs_ids(), [7])
        self.assertEqual(graph.get_nodes_ids(), [5, 6, 7, 8, 9])
         
        #verifying that node ids are changed and their parents' and children's as well
        self.assertEqual(graph.get_id_node_map()[5].get_label(), '0i')
        self.assertEqual(graph.get_id_node_map()[5].get_id(), 5)
        self.assertEqual(graph.get_id_node_map()[5].get_parents(), {8:1})
        self.assertEqual(graph.get_id_node_map()[5].get_children(), {6:1, 7:2})

        self.assertEqual(graph.get_id_node_map()[6].get_label(), '1i')
        self.assertEqual(graph.get_id_node_map()[6].get_id(), 6)
        self.assertEqual(graph.get_id_node_map()[6].get_parents(), {5:1})
        self.assertEqual(graph.get_id_node_map()[6].get_children(), {8:3})

        self.assertEqual(graph.get_id_node_map()[7].get_label(), '2o')
        self.assertEqual(graph.get_id_node_map()[7].get_id(), 7)
        self.assertEqual(graph.get_id_node_map()[7].get_parents(), {5:2})
        self.assertEqual(graph.get_id_node_map()[7].get_children(), {})

        self.assertEqual(graph.get_id_node_map()[8].get_label(), '3a')
        self.assertEqual(graph.get_id_node_map()[8].get_id(), 8)
        self.assertEqual(graph.get_id_node_map()[8].get_parents(), {6:3, 9:1})
        self.assertEqual(graph.get_id_node_map()[8].get_children(), {5:1})

        self.assertEqual(graph.get_id_node_map()[9].get_label(), '4i')
        self.assertEqual(graph.get_id_node_map()[9].get_id(), 9)
        self.assertEqual(graph.get_id_node_map()[9].get_parents(), {})
        self.assertEqual(graph.get_id_node_map()[9].get_children(), {8:1})



class GraphWritingTest(unittest.TestCase):
    def test_read_write_graph(self):
        n0 = node(0, '0i', {3:1}, {1:1, 2:2})
        n1 = node(1, '1i', {0:1}, {3:3})
        n2 = node(2, '2o', {0:2}, {})
        n3 = node(3, '3a', {1:3, 4:1}, {0:1})
        n4 = node(4, '4i', {}, {3:1})
        graph = open_digraph([4], [2], 
                          [n0, n1, n2, n3, n4])
        graph.save_as_dot_file("./test_dot.dot")
        mat = graph.adjacancy_matrix()

        read_graph = graph.from_dot_file("./test_dot.dot")
        read_mat = read_graph.adjacancy_matrix()

        graph.is_well_formed()

        self.assertEqual(len(graph.get_nodes_ids()), len(read_graph.get_nodes_ids()))
        self.assertEqual(len(graph.get_inputs_ids()), len(read_graph.get_inputs_ids()))
        self.assertEqual(len(graph.get_outputs_ids()), len(read_graph.get_outputs_ids()))
        self.assertEqual(mat, read_mat)
        os.remove("./test_dot.dot")


class BoolCircTests(unittest.TestCase):
    def test_acyclic(self):
        n0 = node(0, '0i', {3:1}, {1:1, 2:2})
        n1 = node(1, '1i', {0:1}, {3:3})
        n2 = node(2, '2o', {0:2}, {})
        n3 = node(3, '3a', {1:3, 4:1}, {0:1})
        n4 = node(4, '4i', {}, {3:1})
        graph = open_digraph(
                [4], [2], [n0, n1, n2, n3, n4]
            )
        
        self.assertEqual(graph.is_acyclic(), False)
        self.assertEqual(graph.is_cyclic(), True)

    def test_acyclic_2(self):
        n0 = node(0, 'x0', {}, {4:4})
        n1 = node(1, 'x1', {}, {5:5} )
        n2 = node(2, 'x2', {}, {3:3})
        n3 = node(3, 'copy', {2:2}, {4:4, 7:7})
        n4 = node(4, '|', {0:0, 3:3}, {6:6})
        n5 = node(5, 'copy', {1:1}, {6:6, 7:7})
        n6 = node(6, '|', {4:4, 5:5}, {9:9})
        n7 = node(7, '&', {5:5, 3:3},{8:8})
        n8 = node(8, '~', {7:7}, {9:9})
        n9 = node(9, '&', {6:1, 8:1}, {})

        circuit = open_digraph(
                [0,1,2], [9], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]

                )

        self.assertEqual(circuit.is_acyclic(), True)
        self.assertEqual(circuit.is_cyclic(), False)
    
    def test_is_well_formed(self):
        n0 = node(0, '0', {}, {1: 1})
        n1 = node(1, '', {0: 1}, {2: 1})
        n2 = node(2, '&', {1: 1}, {3: 1})
        n3 = node(3, '~', {2: 1}, {4: 1})
        n4 = node(4, '1', {3: 1}, {})
        valid_circ = bool_circ(open_digraph([0], [4], [n0, n1, n2, n3, n4]))
        self.assertTrue(valid_circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_invalid_node_name_circuit(self):

        # invalid name
        n0 = node(0, '0', {}, {1: 1})
        n1 = node(1, 'lab', {0: 1}, {2: 1})
        n2 = node(2, '&', {1: 1}, {3: 1})
        n3 = node(3, '~', {2: 1}, {})  
        n4 = node(4, '1', {}, {}) 
        invalid_circ = bool_circ(open_digraph([0], [4], [n0, n1, n2, n3, n4]))
        self.assertTrue(invalid_circ.is_empty(), "The invalid circuit should not be well formed thus empty.")

        invalid_circ = bool_circ(open_digraph([0], [4], [n0, n1, n2, n3, n4]), debug=True)
        self.assertNotEqual(len(invalid_circ.get_nodes()), 0)
        self.assertFalse(invalid_circ.is_well_formed(), "The invalid circuit should not be well formed thus empty.")
        

    def test_invalid_outputs_number(self):
        n0 = node(0, '0', {}, {1: 1})
        n1 = node(1, '^', {0: 1}, {2: 2})
        n2 = node(2, '&', {1: 2}, {3: 1})
        n3 = node(3, '~', {2: 1}, {})  
        n4 = node(4, '1', {}, {}) 
        invalid_circ = bool_circ(open_digraph([0], [4], [n0, n1, n2, n3, n4]))
        self.assertTrue(invalid_circ.is_empty(), "The invalid circuit should not be well formed thus empty.")

        invalid_circ = bool_circ(open_digraph([0], [4], [n0, n1, n2, n3, n4]), debug=True)
        self.assertNotEqual(len(invalid_circ.get_nodes()), 0)
        self.assertFalse(invalid_circ.is_well_formed(), "The invalid circuit should not be well formed thus empty.")


    def test_bad_graph_empty(self):
        n0 = node(0, '0i', {3:1}, {1:1, 2:2})
        n1 = node(1, '1i', {0:1}, {3:3})
        n2 = node(2, '2o', {0:2}, {})
        n3 = node(3, '3a', {1:3, 4:1}, {0:1})
        n4 = node(4, '4i', {}, {3:1})
        graph = open_digraph(
                [4], [2], [n0, n1, n2, n3, n4]
            )
        circ = bool_circ(graph)
        self.assertEqual(circ.is_empty(), True)
        
class TestGraphOperations(unittest.TestCase):

    def setUp(self):
        # A simple graph for baseline tests
        # Graph g1: 0 -> 1, input=[0], output=[1]
        self.g1 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[
                node(0, 'a', {}, {1:1}),
                node(1, 'b', {0:1}, {})
            ]
        )
        # Graph g2: 0 -> 1, input=[0], output=[1]
        self.g2 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[
                node(0, 'c', {}, {1:1}),
                node(1, 'd', {0:1}, {})
            ]
        )

    def test_iparallel(self):
        # Test the in-place parallel addition (iparallel)
        original_node_count = len(self.g1.get_nodes_ids())
        # g2 will be copied and its indices shifted by (max id of g1)+1.
        # In g1, max id = 1 so shift by 2: g2's nodes become 2 and 3.
        self.g1.iparallel(self.g2)
        # Verify total nodes: 2 (g1) + 2 (g2) = 4
        self.assertEqual(len(self.g1.get_nodes_ids()), 4)
        # Check that new node ids 2 and 3 exist
        self.assertIn(2, self.g1.get_nodes_ids())
        self.assertIn(3, self.g1.get_nodes_ids())
        # Check inputs: original g1 had [0]; g2’s input (0 shifted to 2) should be added.
        self.assertEqual(set(self.g1.get_inputs_ids()), set([0,2]))
        # Check outputs: original g1 had [1]; g2’s output (1 shifted to 3) should be added.
        self.assertEqual(set(self.g1.get_outputs_ids()), set([1,3]))

    def test_parallel(self):
        # Test parallel returns a new graph, leaving originals unchanged.
        # g1.parallel(g2) should return a graph with all the nodes combined.
        g_parallel = self.g1.parallel(self.g2)
        # g1 still should have its original 2 nodes.
        self.assertEqual(len(self.g1.get_nodes_ids()), 2)
        # New graph should have 4 nodes.
        self.assertEqual(len(g_parallel.get_nodes_ids()), 4)
        # Check that the parallel graph has inputs and outputs from both:
        self.assertEqual(set(g_parallel.get_inputs_ids()), set([0,2]))
        self.assertEqual(set(g_parallel.get_outputs_ids()), set([1,3]))

    def test_icompose(self):
        # icompose merges self with graph g (passed as parameter)
        # For composition, ensure self.get_inputs_ids() has same length as g.get_outputs_ids()
        # We create g1 and a new graph g3 such that g3.outputs has one element.
        n0 = node(0, 'x', {}, {1:1})
        n1 = node(1, 'y', {0:1}, {})
        g_comp1 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[n0, n1]
        )
        # g3: single edge graph: 0 -> 1, with input=[0] and output=[1]
        n2 = node(0, 'p', {}, {1:1})
        n3 = node(1, 'q', {0:1}, {})
        g_comp2 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[n2, n3]
        )
        # For icompose, require len(g_comp1.inputs)==len(g_comp2.outputs) [both 1]
        # In icompose, g_comp2 will be shifted by (g_comp1.max_id()+1).
        # Here, g_comp1.max_id() is 1 so shift = 2 and then:
        #   g_comp2: nodes become 2 and 3, with input=[2] and output=[3].
        # Also, an edge is added from output (3) to the original input (0)
        g_comp1.icompose(g_comp2)
        # Check combined node count: original 2 + composed 2 = 4
        self.assertEqual(len(g_comp1.get_nodes_ids()), 4)
        # Check that node 3 (shifted output) now is a parent of node 0.
        self.assertIn(3, g_comp1.get_id_node_map()[0].get_parents())
        # After icompose, inputs are updated to g_comp2's shifted input [2].
        self.assertEqual(g_comp1.get_inputs_ids(), [2])

    def test_compose(self):
        # Test compose which returns a new graph resulting from composition.
        # Use similar graphs as in test_icompose.
        n0 = node(0, 'x', {}, {1:1})
        n1 = node(1, 'y', {0:1}, {})
        g_comp1 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[n0, n1]
        )
        n2 = node(0, 'p', {}, {1:1})
        n3 = node(1, 'q', {0:1}, {})
        g_comp2 = open_digraph(
            inputs=[0],
            outputs=[1],
            nodes=[n2, n3]
        )
        composed = g_comp1.compose(g_comp2)
        # Ensure that neither original graph was mutated.
        self.assertEqual(len(g_comp1.get_nodes_ids()), 2)
        self.assertEqual(len(g_comp2.get_nodes_ids()), 2)
        # Composed graph should have 4 nodes.
        self.assertEqual(len(composed.get_nodes_ids()), 4)
        # Check that the composition edge exists.
        # g_comp2 shifts: node 1 becomes 3; expect an edge from 3 to original input (0) in g_comp1.
        self.assertIn(3, composed.get_id_node_map()[0].get_parents())
        # Composed inputs are taken from g_comp2 (shifted input should be 2)
        self.assertEqual(composed.get_inputs_ids(), [2])

    def test_identity(self):
        # Test the identity method with n elements.
        n = 4
        ident = open_digraph.identity(n)
        # For each of n iterations, identity adds one node (as input)
        # and then adds an output node. So the total node count is 2*n.
        self.assertEqual(len(ident.get_nodes_ids()), 2 * n)
        self.assertEqual(len(ident.get_inputs_ids()), n)
        self.assertEqual(len(ident.get_outputs_ids()), n)
        # For each output node, check that it has exactly one parent.
        for out_id in ident.get_outputs_ids():
            parents = ident.get_id_node_map()[out_id].get_parents()
            self.assertEqual(len(parents), 1)
            # and that the parent is in the inputs of the identity graph? (not necessarily same id,
            # but typically the output node comes from an input added in the same iteration)
            par = list(parents.keys())[0]
            self.assertIn(par, ident.get_nodes_ids())

    def test_connected_components(self):
        # Create a graph with two disconnected components.
        # Component 1: 0 -> 1; Component 2: 2 -> 3 -> 4
        comp_graph = open_digraph.empty()
        # Add nodes for comp1
        n0 = comp_graph.add_node('comp1_a')
        n1 = comp_graph.add_node('comp1_b')
        comp_graph.add_edge(n0, n1)
        # Add nodes for comp2
        n2 = comp_graph.add_node('comp2_a')
        n3 = comp_graph.add_node('comp2_b')
        n4 = comp_graph.add_node('comp2_c')
        comp_graph.add_edge(n2, n3)
        comp_graph.add_edge(n3, n4)
        total_nodes = set(comp_graph.get_nodes_ids())
        count, components = comp_graph.connected_components()
        # We expect 2 connected components.
        self.assertEqual(count, 2)
        # Validate that the union of components is the full set of nodes.
        comp_nodes = set()
        for comp in components.values():
            comp_nodes.update(comp)
        self.assertEqual(comp_nodes, total_nodes)

    def test_split(self):
        # Using the graph from test_connected_components.
        split_graphs = None
        comp_graph = open_digraph.empty()
        # Component 1: 0 -> 1
        n0 = comp_graph.add_node('comp1_a')
        n1 = comp_graph.add_node('comp1_b')
        comp_graph.add_edge(n0, n1)
        # Component 2: 2 -> 3 -> 4
        n2 = comp_graph.add_node('comp2_a')
        n3 = comp_graph.add_node('comp2_b')
        n4 = comp_graph.add_node('comp2_c')
        comp_graph.add_edge(n2, n3)
        comp_graph.add_edge(n3, n4)
        split_graphs = comp_graph.split()
        # The split() method should return a list with 2 graphs
        self.assertEqual(len(split_graphs), 2)
        # Collect all node ids from split graphs and compare to original

        for graph in split_graphs[0].get_nodes():
            self.assertIn(graph.get_label(), ["comp1_a", "comp1_b"])
        for graph in split_graphs[1].get_nodes():
            self.assertIn(graph.get_label(), ["comp2_a", "comp2_b", "comp2_c"])
            
        self.assertEqual(len(split_graphs[0].get_nodes()), 2)
        self.assertEqual(len(split_graphs[1].get_nodes()), 3)


if __name__ == "__main__":
    unittest.main()
