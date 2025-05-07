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

class ParenthesesTest(unittest.TestCase):
    def test_fusion(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:1, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )

        # node 4
        self.assertEqual(graph_s.get_id_node_map()[4].get_id(), 4)
        self.assertEqual(graph_s.get_id_node_map()[4].get_label(), '|')
        self.assertEqual(graph_s.get_id_node_map()[4].get_parents(), {0:1, 3:1})
        self.assertEqual(graph_s.get_id_node_map()[4].get_children(), {6:1})

        # node 3
        self.assertEqual(graph_s.get_id_node_map()[3].get_id(), 3)
        self.assertEqual(graph_s.get_id_node_map()[3].get_label(), 'copy')
        self.assertEqual(graph_s.get_id_node_map()[3].get_parents(), {2:1})
        self.assertEqual(graph_s.get_id_node_map()[3].get_children(), {4:1, 7:1})

        graph_s.fuse_nodes(4, 3, "h")
        self.assertEqual(graph_s.get_id_node_map()[4].get_id(), 4)
        self.assertEqual(graph_s.get_id_node_map()[4].get_label(), 'h')
        self.assertEqual(graph_s.get_id_node_map()[4].get_parents(), {0:1, 2:1})
        self.assertEqual(graph_s.get_id_node_map()[4].get_children(), {6:1, 7:1})

        self.assertNotIn(3, graph_s.get_nodes_ids())

    def test_fusion_preserving_name(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:1, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )

        # node 4
        self.assertEqual(graph_s.get_id_node_map()[4].get_id(), 4)
        self.assertEqual(graph_s.get_id_node_map()[4].get_label(), '|')
        self.assertEqual(graph_s.get_id_node_map()[4].get_parents(), {0:1, 3:1})
        self.assertEqual(graph_s.get_id_node_map()[4].get_children(), {6:1})

        # node 3
        self.assertEqual(graph_s.get_id_node_map()[3].get_id(), 3)
        self.assertEqual(graph_s.get_id_node_map()[3].get_label(), 'copy')
        self.assertEqual(graph_s.get_id_node_map()[3].get_parents(), {2:1})
        self.assertEqual(graph_s.get_id_node_map()[3].get_children(), {4:1, 7:1})

        graph_s.fuse_nodes(4, 3)
        self.assertEqual(graph_s.get_id_node_map()[4].get_id(), 4)
        self.assertEqual(graph_s.get_id_node_map()[4].get_label(), '|')
        self.assertEqual(graph_s.get_id_node_map()[4].get_parents(), {0:1, 2:1})
        self.assertEqual(graph_s.get_id_node_map()[4].get_children(), {6:1, 7:1})

        self.assertNotIn(3, graph_s.get_nodes_ids())

    def test_fusion_preserving_name_2(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:1, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )

        # node 4
        self.assertEqual(graph_s.get_id_node_map()[4].get_id(), 4)
        self.assertEqual(graph_s.get_id_node_map()[4].get_label(), '|')
        self.assertEqual(graph_s.get_id_node_map()[4].get_parents(), {0:1, 3:1})
        self.assertEqual(graph_s.get_id_node_map()[4].get_children(), {6:1})

        # node 3
        self.assertEqual(graph_s.get_id_node_map()[3].get_id(), 3)
        self.assertEqual(graph_s.get_id_node_map()[3].get_label(), 'copy')
        self.assertEqual(graph_s.get_id_node_map()[3].get_parents(), {2:1})
        self.assertEqual(graph_s.get_id_node_map()[3].get_children(), {4:1, 7:1})

        graph_s.fuse_nodes(3, 4)
        self.assertEqual(graph_s.get_id_node_map()[3].get_id(), 3)
        self.assertEqual(graph_s.get_id_node_map()[3].get_label(), 'copy')
        self.assertEqual(graph_s.get_id_node_map()[3].get_children(), {6:1, 7:1})
        self.assertEqual(graph_s.get_id_node_map()[3].get_parents(), {0:1, 2:1})

        self.assertNotIn(4, graph_s.get_nodes_ids())

if __name__ == "__main__":
    unittest.main()
