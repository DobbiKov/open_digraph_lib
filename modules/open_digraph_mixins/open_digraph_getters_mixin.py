from modules.node import node
from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")


class OpenDigraphGettersMixin(object):
    def get_inputs_ids(self: T) -> list[int]:
        """
        Returns list of ids of input nodes
        """
        return self.inputs
    def get_outputs_ids(self: T) -> list[int]:
        """
        Returns list of ids of output nodes
        """
        return self.outputs
    def get_id_node_map(self: T) -> dict[int, node]:
        """
        Returns dictonary of the form {node_id:node} 
        """
        return self.nodes
    def get_nodes(self: T) -> list[node]:
        """
        Returns list of nodes
        """
        return list(self.nodes.values())
    def get_nodes_ids(self: T) -> list[int]:
        """
        Returns list of ids of all the nodes
        """
        return list(self.nodes.keys())
    def get_number_of_nodes(self: T) -> int:
        """
        Returns number of nodes in the graph
        """
        return len(self.nodes)

    def __getitem__(self: T, i) -> node | None:
        """
        Allow accessing a node by its ID using indexing.

        Args:
            i (int): The ID of the node to retrieve.

        Returns:
            node or None: The node with the specified ID, or None if not found.
        """
        r = filter(lambda x: x.get_id() == i, self.nodes.values())
        r = list(r)
        if(len(r)==0):
            return None
        if(len(r)>1):
            raise RuntimeError(f"Digraph has 2 elements with the same id {i}")
        return r[0] 
    def get_nodes_by_ids(self: T, ids: list[int]) -> list[node]:
        """
        Gives list of nodes by with ids from given list

        Args:
            ids(list[int]): list of ids of nodes

        Returns:
            list[node] - list of nodes with gives ids
        """
        id_node_map = self.get_id_node_map()
        return [id_node_map[i] for i in ids]

    def get_node_id_to_enumerate_mapping(self: T, without_inputs=False, without_outputs=False):
        """
        Creates a mapping node_id to id in [0, n-1] where n is the number of nodes 

        Args:
            without_inputs: bool - set True if you don't want to count input nodes
            without_outputs: bool - set True if you don't want to count output nodes
        Returns:
            dict[int, int] ({node_id:id}) where node_id is the id of a node and id it's id in the matrix
        """
        res = {}

        node_id_mapping = self.get_id_node_map()
        inputs_ids = self.get_inputs_ids()
        outputs_ids = self.get_outputs_ids()

        id = 0

        for node_id in node_id_mapping.keys():
            if without_inputs is True and node_id in inputs_ids:
                continue
            if without_outputs is True and node_id in outputs_ids:
                continue
            res[node_id] = id
            id += 1

        return res
