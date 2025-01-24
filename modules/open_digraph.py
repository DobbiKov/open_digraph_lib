class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

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
        self.children[id] = id
    def add_parent_id(self, id):
        self.parents[id] =id


    def __str__(self):
        res = f"node: {self.get_id()} with label: {self.get_label()}"
        return res
    def __repr__(self):
        return self.__str__()

    def copy(self):
        return node(self.get_id(), self.get_label(), self.get_parents().copy(), self.get_children().copy())
     
class open_digraph: #for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        
    #Getters
    def get_inputs_ids(self):
        return self.inputs
    def get_outputs_ids(self):
        return self.outputs
    def get_id_node_map(self):
        return self.nodes
    def get_nodes(self):
        return list(self.nodes.values)
    def get_nodes_ids(self):
        return list(self.nodes.keys())
    def __getitem__(self, i):
        r = filter(self.nodes, lambda x: x.get_id() == i)
        if(len(r)==0):
            return None
        if(len(r)>1):
            raise RuntimeError(f"Digraph has 2 elements with the same id {i}")
        return r[0] 
    def get_nodes_by_ids(self, ids):
        return [self[i] for i in ids]

    def set_inputs(self, inputs): self.inputs = inputs
    def set_outputs(self, outputs): self.outputs = outputs
    def add_input_id(self, id): 
        self.inputs.append(id)
    def add_output_id(self, id): 
        self.outputs.append(id)


    def __str__(self):
        res = ""
        res += "graph:\n"
        res += "\tInputs:\n"
        res += "\t\t"
        for i in self.get_inputs():
            res += f"{i} "
        res+="\n"

        res += "\tOutputs:\n"
        res += "\t\t"
        for i in self.get_outputs():
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
        return open_digraph([], [], [])
    def copy(self):
        return open_digraph(self.get_inputs_ids().copy(), self.get_outputs_ids().copy(), self.get_nodes().copy())

