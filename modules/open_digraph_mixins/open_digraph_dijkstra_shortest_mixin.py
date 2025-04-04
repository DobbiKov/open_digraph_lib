from modules.node import node

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphDijkstraShortestMixin(object):
    def common_ancestors(self: T, n1: int , n2: int) -> dict[int,tuple[int,int]]:
        """
        Common_ansestors returns a dictionary that contains common nodes of two given nodes, along with distances to each of them

        Args:
            n1(int) = id of a first node
            n2(int) = id of a second node
        Returns:
            {node_id:(distance_to_the_node_1, distance_to_the_node_2)}
        """
        assert n1 in self.get_nodes_ids()
        assert n2 in self.get_nodes_ids()

        dist1, _ = self.dijkstra(n1, direction=-1)
        dist2, _ = self.dijkstra(n2,direction=-1)

        common = set(dist1.keys()) & set(dist2.keys())

        result = {ans: (dist1[ans], dist2[ans]) for ans in common}

        return result

    def dijkstra(self: T, src: int, direction: None | int, tgt: None | int = None) -> tuple[dict[int, int], dict[int, int]]:
        """
        Dijsktra algorithm that returns a dictionary of nodes accessible from the given node *src* with values of distances to those accessible nodes

        Args:
            src(int) = id of the node to count distances for
            direction(None, -1, 1) = direction in which to count distances (-1 = parents only, 1 = children only, None = both)
            tgt(None or int) = None if count distances to each accessible node. Or id to the node we're interested to count the shortest path to
        Returns:
            ({node_id:distance_to_the_node}, {node_id:id_of_prev_node_we_counted_shortest_dist_from})
        """
        assert src in self.get_nodes_ids()
        assert direction == None or direction == 1 or direction == -1
        assert tgt == None or tgt in self.get_nodes_ids()
        Q = [src]
        dist = {src: 0}
        prev = {}
        while len(Q) != 0:
            u = min(Q, key=lambda x: dist[x])

            # if u = tgt, then we found shortest path to tgt, we can stop here
            if tgt != None and u == tgt:
                return dist, prev

            Q.remove(u)
            neighbours = []
            if direction == None or direction == -1:
                for n_id in self.get_id_node_map()[u].get_parents().keys():
                    neighbours.append(n_id)
            if direction == None or direction == 1:
                for n_id in self.get_id_node_map()[u].get_children().keys():
                    neighbours.append(n_id)

            for v in neighbours:
                if v not in dist.keys():
                    Q.append(v)
                if v not in dist.keys() or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return dist, prev

    def shortest_path(self: T, src: int, tgt: int, direction: None | int = None) -> list[int] | None:
        """
        Calculates the shortest path from the source node (*src*) to the target node (*tgt*).

        Args:
            src(int) = id of the source node
            tgt(int) = id of the target node
            direction(None, -1, 1) = direction in which to count distances (-1 = parents only, 1 = children only, None = both)
        Returns:
            list(int) = the path or None if there's no existing path from *src* to *tgt*
        """
        dist, prev = self.dijkstra(src, direction, tgt)
        res = []
        curr_n = tgt
        if src not in dist.keys() or tgt not in dist.keys():
            return None
        while curr_n != src:
            res.append(curr_n)
            curr_n = prev[curr_n]

        res.append(src)

        return list(reversed(res))
