import copy
from modules.open_digraph import node, open_digraph

class bool_circ(open_digraph):
    def __init__(self, g: open_digraph):
        super().__init__(g.inputs, g.outputs, list(g.nodes.values()))
        if not self.is_well_formed():
            self = self.empty()

    
    def is_well_formed(self):
        """
        Tests if a graph is well formed:
            - The graph is acyclic
            -Degree constraints:
                - '' (copy) - indegree = 1
                - '&' (and), '|' (or), '^' (xor) - outdegree = 1
                - '~' (not) - indegree = 1, outdegree = 1
                - '1', '0' - indegree = 0

        Returns:
            True - if the graph is well formed
            False - otherwise
        """
        if not super().is_well_formed():
            return False

        if not self.is_acyclic():
            return False

        for node in self.get_nodes():
            label = node.get_label()
            in_d = node.indegree()
            out_d = node.outdegree()
            node_d = node.degree()

            if label == '':
                if in_d != 1:
                    return False
            elif label in {'&', '|','^'}:
                if out_d != 1:
                    return False
            elif label == '~':
                if out_d != 1 or in_d != 1:
                    return False
            elif label in  {'1', '0'}:
                if out_d != 0:
                    return False
            else: 
                return False
        return True


    

