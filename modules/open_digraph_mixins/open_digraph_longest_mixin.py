from modules.node import node
from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphLongestMixin(object):
    def sort_topologicly(self: T) -> list[list[int]]:
        """
        Sorts the graph topologicly and returns list of lists of ids in the compressed to the top order

        Returns:
            list[list[int]]
        """
        assert self.is_acyclic()
        g = self.copy()

        g.remove_nodes_by_id(g.get_inputs_ids())
        g.remove_nodes_by_id(g.get_outputs_ids())

        def without_parents(graph):
            res = []
            for idx in graph.get_nodes_ids():
                if len( graph.get_id_node_map()[idx].get_parents() ) == 0:
                    res.append(idx)
            return res

        res = []
        while not g.is_empty():
            w_out_parents = without_parents(g)
            assert len(w_out_parents) != 0
            res.append(w_out_parents)
            g.remove_nodes_by_id(w_out_parents)
        return res
    def get_node_depth(self: T, node_id: int) -> None | int:
        """
        Returns a depth of the given node (minimum: 1)

        Args: 
            node_id(int) - id of the node
        Returns:
            int - the depth of the given node
        """
        g_sort = self.sort_topologicly()
        idx = 1 
        for l in g_sort:
            if node_id in l:
                return idx
            idx += 1
        return None

    def get_graph_depth(self: T) -> int:
        """
        Returns the graph's depth (minimum: 1 except if the graph is empty, then 0)
        """
        return len(self.sort_topologicly())

    def longest_path(self: T, u: int, v: int) -> tuple[int, list[int]] | None:
        """
        Returns longest path with it's length between two nodes

        Args:
            u(int) - the starting node
            v(int) - the ending node
        Returns:
            (int, list(int)) - (length, path)
        """
        assert u in self.get_nodes_ids() and v in self.get_nodes_ids()
        def get_path_by_dict(d, n_from, n_to):
            res = [n_to]
            curr = n_to
            while curr != n_from:
                curr = d[curr]
                res.append(curr)
            res.reverse()
            return res
        dist = {u: 0}
        prev = {u: u}

        k = -1
        sort_ls = self.sort_topologicly()
        for i, l in enumerate(sort_ls):
            if u in l:
                k = i
                break
        if k == -1:
            return None
        for i in range(k+1, len(sort_ls)):
            l = sort_ls[i]
            for w in l:
                curr_d = dist[w] if w in dist.keys() else -1
                for p_id in self.get_id_node_map()[w].get_parents():
                    if p_id not in dist.keys():
                        continue
                    if dist[p_id] + 1 < curr_d:
                        continue
                    dist[w] = dist[p_id] + 1
                    prev[w] = p_id
                if w == v:
                    return (dist[v], get_path_by_dict(prev, u, v))
        return None
