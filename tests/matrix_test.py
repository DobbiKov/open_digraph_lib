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
        g = open_digraph.from_matrix(mat)
        g.assert_is_well_formed()

    def test_graph_from_empty_adjacency_matrix(self):
        mat = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        g = open_digraph.from_matrix(mat)
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
        g = open_digraph.from_matrix(mat)
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

if __name__ == "__main__":
    unittest.main()
