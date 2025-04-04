import copy

from modules.open_digraph_mixins.open_digraph_adders_mixin import OpenDigraphAddersMixin
from modules.open_digraph_mixins.open_digraph_compose_parallel_split_mixin import OpenDigraphComposeParallelSplitMixin
from modules.open_digraph_mixins.open_digraph_dijkstra_shortest_mixin import OpenDigraphDijkstraShortestMixin
from modules.open_digraph_mixins.open_digraph_file_display_mixin import OpenDigraphFileDisplayMixin
from modules.open_digraph_mixins.open_digraph_getters_mixin import OpenDigraphGettersMixin
from modules.open_digraph_mixins.open_digraph_longest_mixin import OpenDigraphLongestMixin
from modules.open_digraph_mixins.open_digraph_matrix_mixin import OpenDigraphMatrixMixin
from modules.open_digraph_mixins.open_digraph_removers_mixin import OpenDigraphRemoversMixin
from modules.open_digraph_mixins.open_digraph_wellformedness_mixin import OpenDigraphWellformednessMixin
from modules.open_digraph_mixins.open_digraph_cyclicity_mixin import OpenDigraphCyclicityMixin
from modules.node import node


from typing import TYPE_CHECKING, Type, TypeVar, cast

T = TypeVar("T", bound="open_digraph")



class open_digraph(OpenDigraphCyclicityMixin, OpenDigraphAddersMixin, OpenDigraphRemoversMixin, OpenDigraphGettersMixin, OpenDigraphFileDisplayMixin, OpenDigraphComposeParallelSplitMixin, OpenDigraphDijkstraShortestMixin, OpenDigraphMatrixMixin, OpenDigraphWellformednessMixin, OpenDigraphLongestMixin): #for open directed graph
    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[node]):
        '''
        Initialize a new open directed graph

        Args:
            inputs: int list; the ids of the input nodes
            outputs: int list; the ids of the output nodes
            nodes: node iter;
        '''
        self.inputs: list[int] = inputs
        self.outputs: list[int] = outputs
        self.nodes: dict[int, node] = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        

    @classmethod
    def identity(cls: Type[T], n) -> 'open_digraph':
        g = cls.empty()
        for _ in range(n):
            id = g.add_node()
            g.add_input_id(id)
            g.add_output_node(id)

        return g

    def min_id(self) -> int:
        """
        Returns the smallest id among all the nodes
        """
        return min(self.get_nodes_ids())
    def max_id(self) -> int:
        """
        Returns the biggest id among all the nodes
        """
        if(self.is_empty()):
            return -1
        return max(self.get_nodes_ids())
    
    def shift_indices(self, n: int) -> None:
        """
        Shifts an id of each node by n
        """
        for node in self.get_nodes():
            node.set_id(node.get_id() + n) # change node's id
            node.set_parents({n_id + n:n_mult for n_id, n_mult in node.get_parents().items()}) # change it's parents ids (saved in dict of this node)
            node.set_children({n_id + n:n_mult for n_id, n_mult in node.get_children().items()}) # change it's children ids (saved in dict of this node)

        # change nodes dict keys to new node's ids in the graph
        self.nodes = {node.id:node for node in self.get_nodes()}
        #change inputs and outputs ids in the list in the graph
        self.inputs = [id + n for id in self.get_inputs_ids()]
        self.outputs = [id + n for id in self.get_outputs_ids()]
    
    def fuse_nodes(self, id1: int, id2: int, label: str | None) -> None:
        """
        Fuses two nodes from two given ids. Default: label from the first id.
        """
        if id1 == id2: #if ids are the same we are doing nothing
            return 

        node1 = self.__getitem__(id1)
        assert node1 is not None
        node2 = self.__getitem__(id2)
        assert node2 is not None

        if label is not None:
            node1.set_label(label)
        
        for parent_id, mult in node2.get_parents():
            for _ in range(mult):
                self.add_edge(parent_id, id1)
        
        for child_id, mult  in node2.get_children():
            for _ in range(mult):
                self.add_edge(id1, child_id)

        self.remove_node_by_id(id2)
        
               

    #Setters
    def set_inputs(self, inputs: list[int]): self.inputs = inputs
    def set_outputs(self, outputs: list[int]): self.outputs = outputs


    def __str__(self):
        """
        Return a string representation of the open directed graph.

        Format:
            graph:
                Inputs:
                    id1 id2 ...
                Outputs:
                    id3 id4 ...
                All nodes:
                    id1 - label1
                    id2 - label2
                    ...
        """
        res = ""
        res += "graph:\n"
        res += "\tInputs:\n"
        res += "\t\t"
        for i in self.get_inputs_ids():
            res += f"{i} "
        res+="\n"

        res += "\tOutputs:\n"
        res += "\t\t"
        for i in self.get_outputs_ids():
            res+=f"{i} "
        res+="\n"

        res += "\tAll nodes:\n"
        for node in self.get_nodes():
            res += f"\t\t{node.get_id()} - {node.get_label()}\n"
        return res
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def empty(cls) -> 'open_digraph':
        """
        Create an empty open directed graph.

        Returns:
            open_digraph: A new instance with no inputs, outputs, or nodes.
        """
        return open_digraph([], [], [])

    def copy(self) -> 'open_digraph':
        """
        Create a deep copy of the open directed graph.

        Returns:
            open_digraph: A new instance with copied inputs, outputs, and nodes.
        """
        return open_digraph(self.get_inputs_ids().copy(), self.get_outputs_ids().copy(), copy.deepcopy(self.get_nodes()))
    
    def find_node_without_children(self) -> node | None:
        """
        Finds a node without children in the graph

        Returns:
            node - if it finds a node without children
            None - if it doesn't find such node
        """
        for node in self.get_nodes():
            if len(node.get_children()) == 0:
                return node
        return None 

    def is_empty(self) -> bool:
        """
        Returns True if the graph is empty and False otherwise
        """
        return len(self.nodes) == 0



    

    






