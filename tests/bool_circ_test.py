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
    
    def test_constant_copy_transformation_zero(self):
        n0 = node(0, '0', {}, {1:1})
        n1 = node(1, '', {0:1}, {2:1, 3:1})
        n2 = node(2, '', {1:1}, {})
        n3 = node(3, '', {1:1}, {})
        circ = bool_circ(open_digraph([0], [], [n0, n1, n2, n3]), debug=True)

        circ.constant_copy_transform(1)

        const_ids = [nid for nid in circ.get_nodes_ids() if circ.get_id_node_map()[nid].get_label() == '0']
        self.assertEqual(len(const_ids), 2)
        children = {nid: list(circ.get_id_node_map()[nid].get_children()) for nid in const_ids}
        self.assertCountEqual(children.values(), [[2], [3]])
        
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")
    
    def test_constant_copy_transformation_one(self):
        n0 = node(0, '1', {}, {1:1})
        n1 = node(1, '', {0:1}, {2:1, 3:1})
        n2 = node(2, '', {1:1}, {})
        n3 = node(3, '', {1:1}, {})
        circ = bool_circ(open_digraph([0], [], [n0, n1, n2, n3]), debug=True)

        circ.constant_copy_transform(1)

        const_ids = [nid for nid in circ.get_nodes_ids() if circ.get_id_node_map()[nid].get_label() == '1']
        self.assertEqual(len(const_ids), 2)
        children = {nid: list(circ.get_id_node_map()[nid].get_children()) for nid in const_ids}
        self.assertCountEqual(children.values(), [[2], [3]])
        
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    
    def test_constant_not_transformation(self):
        n0 = node(0, '1', {}, {1:1})
        n1 = node(1, '~', {0:1}, {2:1})
        n2 = node(2, '', {1:1}, {})
        circ = bool_circ(open_digraph([0], [], [n0, n1, n2]), debug=True)

        circ.constant_not_transform(1)

       
        const_ids = [nid for nid in circ.get_nodes_ids() if circ.get_id_node_map()[nid].get_label() == '0']
        self.assertEqual(len(const_ids), 1)
        self.assertIn(2, circ.get_id_node_map()[const_ids[0]].get_children())
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_and_zero(self):
        n0 = node(0, '0', {}, {2:1})
        n1 = node(1, '1', {}, {2:1})
        n2 = node(2, '&', {0:1, 1:1}, {3:1})
        n3 = node(3, '', {2:1}, {})
        circ = bool_circ(open_digraph([0,1], [], [n0, n1, n2, n3]), debug=True)

        circ.transform_and_zero(2)

        self.assertNotIn(2, circ.get_nodes_ids())

        copy_nodes = [nid for nid in circ.get_nodes_ids()
                      if circ.get_id_node_map()[nid].get_label() == '']
        self.assertEqual(len(copy_nodes), 2)
        cp = copy_nodes[1]
        self.assertIn(cp, circ.get_id_node_map()[1].get_children())

        zeros = [nid for nid in circ.get_nodes_ids()
                 if circ.get_id_node_map()[nid].get_label() == '0']
    
        self.assertTrue(any(3 in circ.get_id_node_map()[z].get_children()
                            for z in zeros))
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_and_one(self):
        n0 = node(0, '1', {}, {2:1})  
        n1 = node(1, '0', {}, {2:1})  
        n2 = node(2, '&', {0:1, 1:1}, {3:1})  # AND 
        n3 = node(3, '', {2:1}, {})  
        circ = bool_circ(open_digraph([0,1], [], [n0, n1, n2, n3]), debug=True)

        circ.transform_and_one(2)

        self.assertNotIn(0, circ.get_nodes_ids())

        self.assertIn(2, circ.get_nodes_ids())

        parents = list(circ.get_id_node_map()[2].get_parents().keys())
        self.assertEqual(len(parents), 1)
        self.assertEqual(parents[0], 1)
        self.assertIn(2, circ.get_id_node_map()[1].get_children())

        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")


    def test_transform_or_zero(self):
        n0 = node(0, '0', {}, {2:1})  
        n1 = node(1, '1', {}, {2:1})  
        n2 = node(2, '|', {0:1, 1:1}, {3:1})  # or 
        n3 = node(3, '', {2:1}, {})  
        circ = bool_circ(open_digraph([0,1], [], [n0, n1, n2, n3]), debug=True)

        circ.transform_or_zero(2)

        self.assertNotIn(0, circ.get_nodes_ids())

        self.assertIn(2, circ.get_nodes_ids())

        parents = list(circ.get_id_node_map()[2].get_parents().keys())
        self.assertEqual(len(parents), 1)
        self.assertEqual(parents[0], 1)
        self.assertIn(2, circ.get_id_node_map()[1].get_children())

        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_or_one(self):
        n0 = node(0, '1', {}, {2:1})
        n1 = node(1, '0', {}, {2:1})
        n2 = node(2, '|', {0:1, 1:1}, {3:1})
        n3 = node(3, '', {2:1}, {})
        circ = bool_circ(open_digraph([0,1], [], [n0, n1, n2, n3]), debug=True)

        circ.transform_or_one(2)

        self.assertNotIn(2, circ.get_nodes_ids())

        copy_nodes = [nid for nid in circ.get_nodes_ids()
                      if circ.get_id_node_map()[nid].get_label() == '']
        self.assertEqual(len(copy_nodes), 2)
        cp = copy_nodes[1]
        self.assertIn(cp, circ.get_id_node_map()[1].get_children())

        ones = [nid for nid in circ.get_nodes_ids()
                 if circ.get_id_node_map()[nid].get_label() == '1']
    
        self.assertEqual(len(ones), 1)
        one_id = ones[0]
        self.assertIn(3, circ.get_id_node_map()[one_id].get_children())
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")
    
    def test_transform_xor_zero_binary(self):
        n0 = node(0, '1', {}, {2:1})
        n1 = node(1, '0', {}, {2:1})
        n2 = node(2, '^', {0:1, 1:1}, {3:1})
        n3 = node(3, '', {2:1}, {})
        circ = bool_circ(open_digraph([0,1], [3], [n0, n1, n2, n3]), debug=True)

        circ.transform_xor_zero(2)

        # XOR 
        self.assertIn(2, circ.get_nodes_ids())
        # no NOT nodes
        self.assertFalse(any(nd.get_label() == '~' for nd in circ.get_nodes()))
        parents_Z = list(circ.get_id_node_map()[3].get_parents().keys())
        self.assertEqual(parents_Z, [2])
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_xor_one_binary(self):
        n0 = node(0, '0', {}, {2:1})
        n1 = node(1, '1', {}, {2:1})
        n2 = node(2, '^', {0:1, 1:1}, {3:1})
        n3 = node(3, '', {2:1}, {})
        circ = bool_circ(open_digraph([0,1], [3], [n0, n1, n2, n3]), debug=True)

        circ.transform_xor_one(2)

        # XOR
        self.assertIn(2, circ.get_nodes_ids())
        # exactly one NOT node created
        nots = [nid for nid in circ.get_nodes_ids() if circ.get_id_node_map()[nid].get_label() == '~']
        self.assertEqual(len(nots), 1)
        not_id = nots[0]
        self.assertIn(not_id, circ.get_id_node_map()[2].get_children())
        self.assertIn(3, circ.get_id_node_map()[not_id].get_children())
        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_in_zero(self):
        # OR gate with no inputs
        n0 = node(0, '|', {}, {2:1})
        n2 = node(2, '', {0:1}, {})
        circ = bool_circ(open_digraph([], [2], [n0, n2]), debug=True)

        circ.transform_in_zero(0)
        self.assertNotIn(0, circ.get_nodes_ids())
        zero_nodes = [nid for nid in circ.get_nodes_ids() 
                     if circ.get_id_node_map()[nid].get_label() == '0']
        self.assertEqual(len(zero_nodes), 1)
        zero_id = zero_nodes[0]
        self.assertIn(2, circ.get_id_node_map()[zero_id].get_children())

        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

        n3 = node(3, '^', {}, {4:1})
        n4 = node(4, '', {3:1}, {})
        circ2 = bool_circ(open_digraph([], [4], [n3, n4]), debug=True)

        circ2.transform_in_zero(3)
        self.assertNotIn(3, circ2.get_nodes_ids())
        zero_nodes = [nid for nid in circ2.get_nodes_ids() 
                     if circ2.get_id_node_map()[nid].get_label() == '0']
        self.assertEqual(len(zero_nodes), 1)
        zero_id = zero_nodes[0]
        self.assertIn(4, circ2.get_id_node_map()[zero_id].get_children())
        self.assertTrue(circ2.is_well_formed(), "The valid circuit should be well formed.")

    def test_transform_in_one(self):
        n0 = node(0, '&', {}, {2:1})
        n2 = node(2, '', {0:1}, {})
        circ = bool_circ(open_digraph([], [2], [n0, n2]), debug=True)

        circ.transform_in_one(0)
        self.assertNotIn(0, circ.get_nodes_ids())
        one_nodes = [nid for nid in circ.get_nodes_ids() 
                    if circ.get_id_node_map()[nid].get_label() == '1']
        self.assertEqual(len(one_nodes), 1)
        one_id = one_nodes[0]
        self.assertIn(2, circ.get_id_node_map()[one_id].get_children())

        self.assertTrue(circ.is_well_formed(), "The valid circuit should be well formed.")

    def test_evaluate_simple(self):
        const0 = node(0, '0', {}, {3:1})
        const1 = node(1, '1', {}, {4:1})
        const0_2 = node(2, '0', {}, {5:1})

        copy_0 = node(3, '', {0:1}, {6:1, 8:1})
        copy_1 = node(4, '', {1:1}, {6:1, 7:1})
        copy_0_2 = node(5, '', {2:1}, {8:1})

        and_gate = node(6, '&', {3:1, 4:1}, {10:1})
        not_gate = node(7, '~', {4:1}, {9:1})
        or_gate = node(8, '|', {3:1, 5:1}, {11:1})

        end_gate = node(9, '', {7:1}, {})
        end_gate_2 = node(10, '', {6:1}, {})
        end_gate_3 = node(11, '', {8:1}, {})
        circ = bool_circ(open_digraph([0, 1, 2], [9, 10, 11],
            [const0, const1, const0_2, copy_0, copy_1, copy_0_2,
             and_gate, not_gate, or_gate, end_gate, end_gate_2, end_gate_3]), debug=True)
        
        circ.evaluate()
        self.assertTrue(circ.is_well_formed(), "Circuit should remain well-formed after evaluation")
        self.assertEqual(len(circ.get_nodes_ids()), 6)
    def test_transform_associative_xor(self):
        n0 = node(0, 'x1', {}, {4: 1})
        n1 = node(1, 'x2', {}, {4: 1})
        n2 = node(2, 'x3', {}, {5: 1})
        n3 = node(3, 'x4', {}, {5: 1})
        n4 = node(4, '^', {0: 1, 1: 1}, {5: 1})
        n5 = node(5, '^', {2: 1, 3: 1, 4: 1}, {6: 1})
        n6 = node(6, 'out', {5: 1}, {})

        graph = open_digraph([0, 1, 2, 3], [6], [n0, n1, n2, n3, n4, n5, n6])
        bc = bool_circ(graph)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 4: 1})
        self.assertEqual(bc[4].get_parents(), {0: 1, 1: 1})
        self.assertEqual(len(bc.get_nodes_ids()), 7)

        bc.transform_associative_xor(4)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 4: 1})
        self.assertEqual(bc[4].get_parents(), {0: 1, 1: 1})
        self.assertEqual(len(bc.get_nodes_ids()), 7)

        bc.transform_associative_xor(5)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 0: 1, 1: 1})
        self.assertFalse(4 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 6)

    def test_transform_associative_xor_2(self):
        n0 = node(0, 'x1', {}, {4: 1})
        n1 = node(1, 'x2', {}, {4: 1})
        n2 = node(2, 'x3', {}, {5: 1})
        n3 = node(3, 'x4', {}, {5: 1})
        n4 = node(4, '^', {0: 1, 1: 1}, {5: 1})
        n5 = node(5, '^', {2: 1, 3: 1, 4: 1, 9: 1}, {6: 1})
        n6 = node(6, 'out', {5: 1}, {})

        n7 = node(7, 'x5', {}, {9: 1})
        n8 = node(8, 'x6', {}, {9: 1})
        n9 = node(9, '^', {7: 1, 8: 1}, {5: 1})

        graph = open_digraph([0, 1, 2, 3, 7, 8], [6], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9])
        bc = bool_circ(graph)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 4: 1, 9: 1})
        self.assertEqual(bc[4].get_parents(), {0: 1, 1: 1})
        self.assertEqual(bc[9].get_parents(), {7: 1, 8: 1})
        self.assertEqual(len(bc.get_nodes_ids()), 10)

        bc.transform_associative_xor(4)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 4: 1, 9: 1})
        self.assertEqual(bc[4].get_parents(), {0: 1, 1: 1})
        self.assertEqual(len(bc.get_nodes_ids()), 10)

        bc.transform_associative_xor(9)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 4: 1, 9: 1})
        self.assertEqual(bc[9].get_parents(), {7: 1, 8: 1})
        self.assertEqual(len(bc.get_nodes_ids()), 10)

        bc.transform_associative_xor(5)
        self.assertEqual(bc[5].get_parents(), {2: 1, 3: 1, 0: 1, 1: 1, 7: 1, 8: 1})
        self.assertFalse(4 in bc.get_nodes_ids())
        self.assertFalse(9 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 8)

    def test_transform_associative_copy(self):
        n0 = node(0, 'x1',   {}, {1:1})
        n1 = node(1, '',     {0:1}, {2:1, 5:1, 6:1})
        n2 = node(2, '',     {1:1}, {3:1, 4:1})
        n3 = node(3, 'out1', {2:1}, {})
        n4 = node(4, 'out2', {2:1}, {})
        n5 = node(5, 'out3', {1:1}, {})
        n6 = node(6, 'out4', {1:1}, {})

        graph = open_digraph([0], [3, 4, 5, 6], [n0, n1, n2, n3, n4, n5, n6])
        bc = bool_circ(graph)
        self.assertEqual(bc[1].get_children(), {2:1, 5:1, 6:1})
        self.assertEqual(bc[2].get_children(), {3:1, 4:1})
        self.assertEqual(len(bc.get_nodes_ids()), 7)

        bc.transform_associative_copy(1)
        self.assertEqual(bc[1].get_children(), {2:1, 5:1, 6:1})
        self.assertEqual(bc[2].get_children(), {3:1, 4:1})
        self.assertEqual(len(bc.get_nodes_ids()), 7)

        bc.transform_associative_copy(2)
        self.assertEqual(bc[1].get_children(), {5:1, 6:1, 3:1, 4:1})
        self.assertFalse(2 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 6)

    def test_transform_involution_xor(self):
        n0 = node(0, 'x1', {}, {3: 1})
        n1 = node(1, 'x2', {}, {3: 1})
        n2 = node(2, 'x3', {}, {4: 1})
        n3 = node(3, '^', {0:1, 1:1, 4:2}, {5: 1})
        n4 = node(4, '', {2:1}, {3:2, 6:1, 7:1})
        n5 = node(5, 'out1', {3:1}, {})
        n6 = node(6, 'out2', {4:1}, {})
        n7 = node(7, 'out3', {4:1}, {})

        graph = open_digraph([0, 1, 2], [5, 6, 7], [n0, n1, n2, n3, n4, n5, n6, n7])
        bc = bool_circ(graph)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:2})
        self.assertEqual(bc[4].get_children(), {3:2, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1})
        self.assertEqual(bc[4].get_children(), {6:1, 7:1})

        # make pair number of edges
        num_of_edges = 4
        for i in range(num_of_edges):
            bc.add_edge(4, 3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:num_of_edges})
        self.assertEqual(bc[4].get_children(), {3:num_of_edges, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1})
        self.assertEqual(bc[4].get_children(), {6:1, 7:1})

        # make more pair number of edges
        num_of_edges = 12 
        for i in range(num_of_edges):
            bc.add_edge(4, 3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:num_of_edges})
        self.assertEqual(bc[4].get_children(), {3:num_of_edges, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1})
        self.assertEqual(bc[4].get_children(), {6:1, 7:1})

    def test_transform_involution_xor_dont_work(self):
        # won't work cause only one multiplicity
        n0 = node(0, 'x1', {}, {3: 1})
        n1 = node(1, 'x2', {}, {3: 1})
        n2 = node(2, 'x3', {}, {4: 1})
        n3 = node(3, '^', {0:1, 1:1, 4:1}, {5: 1})
        n4 = node(4, '', {2:1}, {3:1, 6:1, 7:1})
        n5 = node(5, 'out1', {3:1}, {})
        n6 = node(6, 'out2', {4:1}, {})
        n7 = node(7, 'out3', {4:1}, {})

        graph = open_digraph([0, 1, 2], [5, 6, 7], [n0, n1, n2, n3, n4, n5, n6, n7])
        bc = bool_circ(graph)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

    def test_transform_involution_xor_odd(self):
        # won't work cause only one multiplicity
        n0 = node(0, 'x1', {}, {3: 1})
        n1 = node(1, 'x2', {}, {3: 1})
        n2 = node(2, 'x3', {}, {4: 1})
        n3 = node(3, '^', {0:1, 1:1, 4:1}, {5: 1})
        n4 = node(4, '', {2:1}, {3:1, 6:1, 7:1})
        n5 = node(5, 'out1', {3:1}, {})
        n6 = node(6, 'out2', {4:1}, {})
        n7 = node(7, 'out3', {4:1}, {})

        graph = open_digraph([0, 1, 2], [5, 6, 7], [n0, n1, n2, n3, n4, n5, n6, n7])
        bc = bool_circ(graph)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

        # make odd number of edges
        bc.remove_parallel_edges(4, 3)
        num_of_edges = 3 
        for i in range(num_of_edges):
            bc.add_edge(4, 3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:num_of_edges})
        self.assertEqual(bc[4].get_children(), {3:num_of_edges, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

        # make more odd number of edges
        bc.remove_parallel_edges(4, 3)
        num_of_edges = 11
        for i in range(num_of_edges):
            bc.add_edge(4, 3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:num_of_edges})
        self.assertEqual(bc[4].get_children(), {3:num_of_edges, 6:1, 7:1})

        bc.transform_involution_xor(3)

        self.assertEqual(bc[3].get_parents(), {0:1, 1:1, 4:1})
        self.assertEqual(bc[4].get_children(), {3:1, 6:1, 7:1})

    def test_transform_erase_operator(self):
        n0 = node(0, 'x1', {}, {3: 1})
        n1 = node(1, 'x2', {}, {3: 1})
        n2 = node(2, 'x3', {}, {3: 1})
        n3 = node(3, '^', {0:1, 1:1, 2:1}, {4:1})
        n4 = node(4, '', {3:1}, {})

        graph = open_digraph([0, 1, 2], [], [n0, n1, n2, n3, n4])
        bc = bool_circ(graph)

        self.assertTrue(4 in bc.get_nodes_ids())
        self.assertTrue(3 in bc.get_nodes_ids())

        self.assertTrue(3 in list(bc[0].get_children().keys()))
        self.assertTrue(3 in list(bc[1].get_children().keys()))
        self.assertTrue(3 in list(bc[2].get_children().keys()))

        bc.transform_erase_operator(4)

        self.assertFalse(4 in bc.get_nodes_ids())
        self.assertFalse(3 in bc.get_nodes_ids())

        self.assertFalse(3 in list(bc[0].get_children().keys()))
        self.assertFalse(3 in list(bc[1].get_children().keys()))
        self.assertFalse(3 in list(bc[2].get_children().keys()))
    
    def test_transform_xor_with_not_parents(self):
        n0 = node(0, 'x1', {}, {3: 1})
        n1 = node(1, 'x2', {}, {6: 1})
        n2 = node(2, 'x3', {}, {4: 1})
        n3 = node(3, '^', {0:1, 4:1, 6:1}, {5:1})
        n4 = node(4, '~', {2:1}, {3:1})
        n5 = node(5, 'out', {3:1}, {})
        n6 = node(6, '~', {1:1}, {3:1})

        graph = open_digraph([0, 1, 2], [5], [n0, n1, n2, n3, n4, n5, n6])
        bc = bool_circ(graph)

        self.assertTrue(bc[3].get_parents(), {0:1, 4:1, 6:1})
        self.assertEqual(bc[4].get_parents(), {2:1})
        self.assertEqual(bc[6].get_parents(), {1:1})
        curr_child = next(iter(bc[3].get_children().keys()))
        self.assertEqual( bc[curr_child].get_label(), 'out' )
        self.assertNotEqual( bc[curr_child].get_label(), '~' )

        bc.transform_xor_if_has_parent_not(3)

        self.assertNotEqual(bc[4].get_parents(), {2:1})
        self.assertNotEqual(bc[6].get_parents(), {1:1})
        self.assertTrue(bc[3].get_parents(), {0:1, 1:1, 2:1})

        curr_child = next(iter(bc[3].get_children().keys()))
        self.assertNotEqual( bc[curr_child].get_label(), 'out' )
        self.assertEqual( bc[curr_child].get_label(), '~' )
        curr_child = next(iter(bc[curr_child].get_children().keys()))
        self.assertEqual( bc[curr_child].get_label(), '~' )
        curr_child = next(iter(bc[curr_child].get_children().keys()))
        self.assertEqual( bc[curr_child].get_label(), 'out' )

    def test_transform_copy_with_not_parents(self):
        n0 = node(0, 'x1', {}, {1:1})
        n1 = node(1, '~',  {0:1}, {2:1})
        n2 = node(2, '',   {1:1}, {3:1, 4:3, 6:1})
        n3 = node(3, 'out1',   {2:1}, {})
        n4 = node(4, '|',   {2:3}, {5:1})
        n5 = node(5, 'out2',   {4:1}, {})
        n6 = node(6, 'out3',   {2:1}, {})

        graph = open_digraph([0], [3, 5, 6], [n0, n1, n2, n3, n4, n5, n6])
        bc = bool_circ(graph)

        self.assertEqual(bc[0].get_children(), {1:1})
        self.assertEqual(bc[2].get_parents(), {1:1})
        self.assertEqual(len(list(bc[2].get_children().keys())), 3)
        for child_id in list(bc[2].get_children().keys()):
            self.assertNotEqual(bc[child_id].get_label(), "~")

        bc.transform_copy_if_has_parent_not(2)

        self.assertEqual(bc[0].get_children(), {2:1})
        self.assertEqual(bc[2].get_parents(), {0:1})
        self.assertEqual(len(list(bc[2].get_children().keys())), 5)
        for child_id in list(bc[2].get_children().keys()):
            self.assertEqual(bc[child_id].get_label(), "~")

    def test_transform_not_involution(self):
        n0 = node(0, 'x1', {}, {1:1})
        n1 = node(1, '~',  {0:1}, {2:1})
        n2 = node(2, '~',   {1:1}, {3:1})
        n3 = node(3, 'out1',   {2:1}, {})

        graph = open_digraph([0], [3], [n0, n1, n2, n3])
        bc = bool_circ(graph)

        self.assertEqual(bc[0].get_children(), {1:1})
        self.assertEqual(bc[3].get_parents(), {2:1})
        self.assertTrue(1 in bc.get_nodes_ids())
        self.assertTrue(2 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 4)

        bc.transform_not_involution(1)

        self.assertEqual(bc[0].get_children(), {1:1})
        self.assertEqual(bc[3].get_parents(), {2:1})
        self.assertTrue(1 in bc.get_nodes_ids())
        self.assertTrue(2 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 4)

        bc.transform_not_involution(2)

        self.assertEqual(bc[0].get_children(), {3:1})
        self.assertEqual(bc[3].get_parents(), {0:1})
        self.assertFalse(1 in bc.get_nodes_ids())
        self.assertFalse(2 in bc.get_nodes_ids())
        self.assertEqual(len(bc.get_nodes_ids()), 2)

if __name__ == "__main__":
    unittest.main()
