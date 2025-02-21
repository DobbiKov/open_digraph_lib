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
        self.assertIsNone(result, "Adding edge with nonexistent source should return None.")
        graph.assert_is_well_formed()
        
        # Attempt to add an edge where target node does not exist
        result = graph.add_edge(2, 999)
        self.assertIsNone(result, "Adding edge with nonexistent target should return None.")
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
        graph = bool_circ([4], [2], 
                          [n0, n1, n2, n3, n4])
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

        circuit = bool_circ(
            [0,1,2], [9], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )

        self.assertEqual(circuit.is_acyclic(), True)
        self.assertEqual(circuit.is_cyclic(), False)

if __name__ == "__main__":
    unittest.main()
