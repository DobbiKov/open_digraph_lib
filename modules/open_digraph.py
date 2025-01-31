class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id: int = identity
        self.label: str = label
        self.parents: dict[int, int] = parents
        self.children: dict[int, int] = children

    #Getters
    def get_id(self): return self.id
    def get_label(self): return self.label
    def get_parents(self): return self.parents
    def get_children(self): return self.children
    
    #Setters
    def set_id(self, v): self.id = v
    def set_label(self, v): self.label = v
    def set_parents(self,v): self.parents = v
    def set_children(self,v): self.children = v

    def add_child_id(self, id):
        if id not in self.get_children().keys():
            self.children[id] = 1
        else:
            self.children[id] += 1

    def add_parent_id(self, id):
        if id not in self.get_parents().keys():
            self.parents[id] = 1
        else:
            self.parents[id] += 1

    #Removers
    def remove_parent_once(self, id):
        if id not in self.get_parents().keys() or self.get_parents()[id] <= 0:
            return
        self.parents[id] -= 1
        if self.get_parents()[id] == 0:
            self.remove_parent_id(id)

    def remove_child_once(self, id):
        if id not in self.get_children().keys() or self.get_children()[id] <= 0:
            return
        self.children[id] -= 1

        if self.get_children()[id] == 0:
            self.remove_child_id(id)

    def remove_parent_id(self, id):
        if id not in self.get_parents().keys():
            return
        self.parents.pop(id)

    def remove_child_id(self, id):
        if id not in self.get_children().keys():
            return
        self.children.pop(id)


    def __str__(self):   #Return a string representation of the node
        res = f"node: {self.get_id()} with label: {self.get_label()}"
        return res
    def __repr__(self): #Return a string representation of the node
        return self.__str__()

    def copy(self):
        """
        Create a deep copy of the node.

        Returns:
            node: A new instance of the node with copied attributes.
        """
        return node(self.get_id(), self.get_label(), self.get_parents().copy(), self.get_children().copy())
     
class open_digraph: #for open directed graph
    def __init__(self, inputs, outputs, nodes):
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
        
    #Getters
    def get_inputs_ids(self):
        return self.inputs
    def get_outputs_ids(self):
        return self.outputs
    def get_id_node_map(self):
        return self.nodes
    def get_nodes(self):
        return list(self.nodes.values())
    def get_nodes_ids(self):
        return list(self.nodes.keys())
    def __getitem__(self, i):
        """
        Allow accessing a node by its ID using indexing.

        Args:
            i (int): The ID of the node to retrieve.

        Returns:
            node or None: The node with the specified ID, or None if not found.
        """
        r = filter(lambda x: x.get_id() == i, self.nodes)
        r = list(r)
        if(len(r)==0):
            return None
        if(len(r)>1):
            raise RuntimeError(f"Digraph has 2 elements with the same id {i}")
        return r[0] 
    def get_nodes_by_ids(self, ids):
        return [self.get_id_node_map()[i] for i in ids]

    #Setters
    def set_inputs(self, inputs): self.inputs = inputs
    def set_outputs(self, outputs): self.outputs = outputs

    #Adders
    def add_input_id(self, id): 
        self.inputs.append(id)
    def add_output_id(self, id): 
        self.outputs.append(id)

    def new_id(self):
        ids = self.get_nodes_ids()
        ids = sorted(ids)
        for i in range(ids[0], ids[-1]):
            if i not in ids:
                return i
        return ids[-1] + 1

    def add_edge(self, src, tgt):
        """
        Add a directed edge from source node to target node.

        Args:
            src (int): Source node ID.
            tgt (int): Target node ID.

        Returns:
            bool: True if the edge was added successfully, False otherwise.
        """
        if src not in self.get_nodes_ids() or tgt not in self.get_nodes_ids():
            return None
        self.nodes[src].add_child_id(tgt)
        self.nodes[tgt].add_parent_id(src)
    def add_node(self, label='', parents=None, children=None):
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
        if parents != None:
            for i in parents.keys():
                for j in range(parents[i]): #we add as many edges as we have multiplicities
                    self.add_edge(i, n_id)
        if children != None:
            for i in children.keys():
                for j in range(children[i]): #we add as many edges as we have multiplicities
                    self.add_edge(n_id, i)
        return n_id

    #removers
    def remove_edge(self, src, tgt):
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

    def remove_parallel_edges(self, src, tgt):
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

    def remove_node_by_id(self, id):
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
            self.inputs.pop(id)
        if id in self.outputs:
            self.outputs.pop(id)

    def remove_edges(self, lst: list[tuple[int, int]]):
        """
        Removes edges provided in the list

        Args:
            lst((int, int) list): a list of tuples (source, target)
        Returns:
            None
        """
        for (src, tgt) in lst:
            self.remove_edge(src, tgt)

    def remove_several_parallel_edges(self, lst: list[tuple[int, int]]):
        """
        Removes all the edges provided in the list

        Args:
            lst((int, int) list): a list of tuples (source, target)
        Returns:
            None
        """
        for (src, tgt) in lst:
            self.remove_parallel_edges(src, tgt)

    def remove_nodes_by_id(self, ids: list[int]):
        """
        Removes all the nodes provided in the list and carefully removes all the edges pointed to and from the nodes.

        Args:
            ids(int list): list on ids of the nodes to delete
        Returns:
            None
        """
        for id in ids:
            self.remove_node_by_id(id)


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
        for n_idx, node in self.get_nodes().items():
            res += f"\t\t{node.get_id()} - {node.get_label()}\n"
        return res
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def empty(cls):
        """
        Create an empty open directed graph.

        Returns:
            open_digraph: A new instance with no inputs, outputs, or nodes.
        """
        return open_digraph([], [], [])
    def copy(self):
        """
        Create a deep copy of the open directed graph.

        Returns:
            open_digraph: A new instance with copied inputs, outputs, and nodes.
        """
        return open_digraph(self.get_inputs_ids().copy(), self.get_outputs_ids().copy(), self.get_nodes().copy())
    
    def assert_is_well_formed(self):
        """
        check if the open directed graph is well-formed.

        raises an assertion error if any condition is violated.
        """

        node_ids = set(self.get_id_node_map().keys())

        for input_id in self.get_inputs_ids():
            assert input_id in node_ids, f"Input {input_id} not in nodes"
        for output_id in self.get_outputs_ids():
            assert output_id in node_ids, f"Output {output_id} not in nodes"

        for input_id in self.get_inputs_ids():
            input_node = self.get_id_node_map()[input_id]
            assert len(input_node.get_parents()) == 0, f"Input {input_id} should have no parents"
            assert len(input_node.get_children()) == 1, f"Input {input_id} should have only one child"
            child_id, multiplicity = next(iter(input_node.get_children().items()))
            assert multiplicity == 1, f"Input {input_id} should have multiplicity 1 to child{child_id}"

        for output_id in self.get_outputs_ids():
            output_node = self.get_id_node_map()[output_id]
            assert len(output_node.get_parents()) == 1, f"Output {output_id} should have only one parent"
            assert len(output_node.get_children()) == 0, f"Output {output_id} should have no children"
            parent_id, multiplicity = next(iter(output_node.get_parents().items()))
            assert multiplicity == 1, f"Output {output_id} should have multiplicity 1 from parent {parent_id}"

        for node_id, node in self.get_id_node_map().items():
            assert node.get_id() == node_id, f"Node id {node_id} does not match its key in nodes"

        for node in self.get_nodes():
            for child_id, multiplicity in node.get_children().items():
                assert child_id in self.get_id_node_map(), f"Node {node.get_id()} has a child {child_id} that does not exist"
                child_node = self.get_id_node_map()[child_id]
                assert node.get_id() in child_node.get_parents(), f"Child {child_id} does not recognize {node.get_id()} as parent"
                assert child_node.get_parents()[node.get_id()] == multiplicity, (
                    f"Inconsistent multiplicity between {node.get_id()} -> {child_id}: "
                    f"{multiplicity} (child should have same multiplicity from parent)"
                )
            for parent_id, multiplicity in node.get_parents().items():
                assert parent_id in self.get_id_node_map(), f"Node {node.get_id()} has a parent {parent_id} that does not exist"
                parent_node = self.get_id_node_map()[parent_id]
                assert node.get_id() in parent_node.get_children(), f"Parent {parent_id} does not recognize {node.get_id()} as child"
                assert parent_node.get_children()[node.get_id()] == multiplicity, (
                    f"Inconsistent multiplicity between {node.get_id()} -> {parent_id}:"
                    f"{multiplicity} (parent should have same muliplicity to child)"
                )
