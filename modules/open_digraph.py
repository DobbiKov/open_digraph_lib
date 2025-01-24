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

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children
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
        self.nodes = {node.id:node for node in nodes} # self.nodse: <int,node> dict

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_nodes(self):
        return self.nodes
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
        return open_digraph(self.get_inputs().copy(), self.get_outputs().copy(), self.get_nodes().copy())

