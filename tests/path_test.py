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

class DijkstraTest(unittest.TestCase):
    def test_dijkstra(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:0, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [0,1,2], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )
        graph_s.add_output_node(9)

        # bidirectional
        dist, prev = graph_s.dijkstra(3, None)
        self.assertEqual(
                dist,
                {3: 0, 2: 1, 4: 1, 7: 1, 0: 2, 6: 2, 5: 2, 8: 2, 9: 3, 1: 3, 10: 4}
        )
        self.assertEqual(
                prev,
                {2: 3, 4: 3, 7: 3, 0: 4, 6: 4, 5: 7, 8: 7, 9: 6, 1: 5, 10: 9}
        )

        # parents only
        dist, prev = graph_s.dijkstra(3, 1)
        self.assertEqual(
                dist,
                {3: 0, 4: 1, 7: 1, 6: 2, 8: 2, 9: 3, 10: 4}
        )
        self.assertEqual(
                prev,
                {4: 3, 7: 3, 6: 4, 8: 7, 9: 6, 10: 9}
        )

        # children only
        dist, prev = graph_s.dijkstra(3, -1)
        self.assertEqual(
                dist,
                {2: 1, 3: 0}
        )
        self.assertEqual(
                prev,
                {2: 3}
        )

        # unreachable nodes
        sh_path = graph_s.shortest_path(3, 5, 1)
        self.assertEqual(sh_path, None)

        # shortes path
        sh_path = graph_s.shortest_path(3, 9, 1)
        self.assertEqual(sh_path, [3, 4, 6, 9])
    def test_common_ancestors(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:0, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [0,1,2], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )
        graph_s.add_output_node(9)
        some_ancestors = graph_s.common_ancestors(6, 8)

        self.assertEqual(some_ancestors, {1: (2, 3), 2: (3, 3), 3: (2, 2), 5: (1, 2)})
        for i in [1, 2, 3, 5]:
            self.assertNotEqual(graph_s.shortest_path(i, 6, 1), None)
            self.assertNotEqual(graph_s.shortest_path(i, 8, 1), None)

        self.assertEqual(graph_s.common_ancestors(3, 5), {})

class LongestPathTest(unittest.TestCase):
    def setUp(self):
        n0 = node(0, 'x0', {}, {4:1})
        n1 = node(1, 'x1', {}, {5:1} )
        n2 = node(2, 'x2', {}, {3:1})
        n3 = node(3, 'copy', {2:1}, {4:1, 7:1})
        n4 = node(4, '|', {0:0, 3:1}, {6:1})
        n5 = node(5, 'copy', {1:1}, {6:1, 7:1})
        n6 = node(6, '|', {4:1, 5:1}, {9:1})
        n7 = node(7, '&', {5:1, 3:1},{8:1})
        n8 = node(8, '~', {7:1}, {9:1})
        n9 = node(9, '&', {6:1, 8:1}, {})

        graph_s = open_digraph(
            [], [], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
        )
        graph_s.add_output_node(9)
        self.g = graph_s
    def test_topological_sort(self):
        res = self.g.sort_topologicly()
        self.assertEqual(res, [[0, 1, 2], [3, 5], [4, 7], [6, 8], [9]])
    def test_cyclic_raises_exception(self):
        n0 = node(0, 'x0', {}, {1:1})
        n1 = node(1, 'x1', {0:1, 3:1}, {2:1})
        n2 = node(2, 'x2', {1:1}, {3:1})
        n3 = node(3, 'x3', {2:1}, {1:1})
        graph = open_digraph([], [], [n0, n1, n2, n3])
        self.assertRaises(AssertionError, graph.sort_topologicly)

    def test_node_depth(self):
        self.assertEqual(self.g.get_node_depth(0), 1)
        self.assertEqual(self.g.get_node_depth(1), 1)
        self.assertEqual(self.g.get_node_depth(2), 1)

        self.assertEqual(self.g.get_node_depth(3), 2)
        self.assertEqual(self.g.get_node_depth(5), 2)

        self.assertEqual(self.g.get_node_depth(4), 3)
        self.assertEqual(self.g.get_node_depth(7), 3)

        self.assertEqual(self.g.get_node_depth(6), 4)
        self.assertEqual(self.g.get_node_depth(8), 4)

        self.assertEqual(self.g.get_node_depth(9), 5)

        self.assertEqual(self.g.get_node_depth(10), None)

    def test_graph_depth(self):
        self.assertEqual(self.g.get_graph_depth(), 5)
        self.assertEqual(open_digraph.empty().get_graph_depth(), 0)

    def test_longest_paht(self):
        (length, path) = self.g.longest_path(1, 9) or (0, [])
        self.assertEqual(length, 4)
        self.assertEqual(path, [1, 5, 7, 8, 9])

        self.assertEqual(self.g.longest_path(1, 2), None)

if __name__ == "__main__":
    unittest.main()
