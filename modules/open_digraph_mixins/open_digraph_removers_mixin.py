from modules.node import node

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphRemoversMixin(object):
    def remove_edge(self: T, src: int, tgt: int) -> None:
        """
        Remove one edge pointing from [src] to [tgt]

        Args:
            src(int): id of the node we point edge from
            tgt(int): id of the node we point edge to 
        Returns:
            None
        """
        self.nodes[src].remove_child_once(tgt)
        self.nodes[tgt].remove_parent_once(src)

    def remove_parallel_edges(self: T, src: int, tgt: int) -> None:
        """
        Remove all the edges pointing from [src] to [tgt]

        Args:
            src(int): id of the node we point edge from
            tgt(int): id of the node we point edge to 
        Returns:
            None
        """
        self.nodes[src].remove_child_id(tgt)
        self.nodes[tgt].remove_parent_id(src)

    def remove_node_by_id(self: T, id: int):
        """
        Remove the node by given id and remove carefully all the edges pointing to or from the given node

        Args:
            id(int): node id
        Returns:
            None
        """
        #removing edges
        if id not in self.get_nodes_ids():
            return
        ids_parents = list(self.get_id_node_map()[id].get_parents().keys())
        for i in ids_parents:
            self.remove_parallel_edges(i, id)

        ids_children = list(self.get_id_node_map()[id].get_children().keys())
        for i in ids_children:
            self.remove_parallel_edges(id, i)

        #removing from lists
        if id in self.nodes.keys():
            self.nodes.pop(id)
        if id in self.inputs:
            self.inputs.remove(id)
        if id in self.outputs:
            self.outputs.remove(id)

    def remove_edges(self: T, lst: list[tuple[int, int]]) -> None:
        """
        Removes edges provided in the list

        Args:
            lst((int, int) list): a list of tuples (source, target)
        Returns:
            None
        """
        for (src, tgt) in lst:
            self.remove_edge(src, tgt)

    def remove_several_parallel_edges(self: T, lst: list[tuple[int, int]]) -> None:
        """
        Removes all the edges provided in the list

        Args:
            lst((int, int) list): a list of tuples (source, target)
        Returns:
            None
        """
        for (src, tgt) in lst:
            self.remove_parallel_edges(src, tgt)

    def remove_nodes_by_id(self: T, ids: list[int]) -> None:
        """
        Removes all the nodes provided in the list and carefully removes all the edges pointed to and from the nodes.

        Args:
            ids(int list): list on ids of the nodes to delete
        Returns:
            None
        """
        for id in ids:
            self.remove_node_by_id(id)
