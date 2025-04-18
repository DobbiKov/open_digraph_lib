from modules.node import node

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphAddersMixin(object):
    def add_input_id(self: T, id: int) -> None: 
        """
        Adds given id to the list of inputs
        """
        self.inputs.append(id)
    def add_output_id(self: T, id: int) -> None: 
        """
        Adds given id to the list of outputs
        """
        self.outputs.append(id)

    def new_id(self: T) -> int:
        """
        Returns availible id in the graph for a new node
        """
        # Proposing simpler code 
        # Les optimal in sens of utilizing all possible ids, but faster
        # return max(self.get_nodes_ids())+1

        ids = self.get_nodes_ids()
        if ids == None or len(ids) == 0:
            return 0

        ids = sorted(ids)
        for i in range(ids[0], ids[-1]):
            if i not in ids:
                return i
        return ids[-1] + 1

    def add_edge(self: T, src: int, tgt: int) -> bool:
        """
        Add a directed edge from source node to target node.

        Args:
            src (int): Source node ID.
            tgt (int): Target node ID.

        Returns:
            bool: True if the edge was added successfully, False otherwise.
        """
        if src not in self.get_nodes_ids() or tgt not in self.get_nodes_ids():
            return False
        self.nodes[src].add_child_id(tgt)
        self.nodes[tgt].add_parent_id(src)
        return True

    def add_edges(self: T, edges):
        for src, tgt in edges:
            self.add_edge(src, tgt)
    
    def add_node(self: T, label='', parents: dict[int, int] | None=None, children: dict[int, int] | None=None) -> int:
        """
        Add a new node to the graph with optional connections.

        Args:
            label (str): Label for the new node.
            parents (dict, optional): Parent node IDs mapped to multiplicities.
            children (dict, optional): Child node IDs mapped to multiplicities.

        Returns:
            int: The ID of the newly added node.
        """
        n_id = self.new_id()
        n = node(n_id, label, {}, {})
        self.nodes[n_id] = n
        # Suggestion/interpretation 
        # Parents and children can be just lists of ids of parents and children respectively, 
        # as a node can have list of parents and list of children, and their multiplicities do not play a role
        # if parents !=None:
        #     self.add_edges(zip(parents, [n_id for _ in range(len(parents))]))
        # if children != None:
        #     self.add_edges(zip([n_id]*len(children), children))
        # return n_id
        # End of suggestion

        if parents != None:
            for i in parents.keys():
                for j in range(parents[i]): #we add as many edges as we have multiplicities
                    self.add_edge(i, n_id)
        if children != None:
            for i in children.keys():
                for j in range(children[i]): #we add as many edges as we have multiplicities
                    self.add_edge(n_id, i)
        return n_id

    def add_input_node(self: T, point_to_id: int, label: str = 'input') -> int:
        """
        Adds a new input node to the graph. Carefully adds the id to input_ids list and creates an edge

        Args:
            point_to_id(int): id of the node, new input node will point to
            label(str)(optional) - label to set for a new input node

        Returns:
            id of the new input node (return -1 if the node couldn't be added)
        """
        if point_to_id not in self.get_nodes_ids():
            return -1
        if point_to_id in self.get_inputs_ids():
            return -1
        new_id = self.add_node(label, {}, {})
        self.add_edge(new_id, point_to_id)
        self.add_input_id(new_id)
        return new_id

    def add_output_node(self: T, point_from_id: int, label: str = 'output') -> int:
        """
        Adds a new output node to the graph. Carefully adds the id to output_ids list and creates an edge

        Args:
            point_from_id(int): id of the node that new input node will be pointed from
            label(str)(optional) - label to set for a new output node

        Returns:
            id of the new output node (return -1 if the node couldn't be added)
        """
        if point_from_id not in self.get_nodes_ids():
            return -1
        if point_from_id in self.get_outputs_ids():
            return -1
        new_id = self.add_node(label, {}, {})
        self.add_edge(point_from_id, new_id)
        self.add_output_id(new_id)
        return new_id
