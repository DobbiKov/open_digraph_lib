import copy
from modules.open_digraph import node, open_digraph

class bool_circ(open_digraph):
    def __init__(self, g: open_digraph):
        super().__init__(g.inputs, g.outputs, g.nodes)

    def is_acyclic_inner(self):
        """
        Helping method for is_acyclique, DON'T USE THIS METHOD OUT OF is_acyclic 
        """
        if self.get_number_of_nodes() == 0:
            return True
        node = self.find_node_without_children()
        match node:
            case None:
                return False

            case _:
                self.remove_node_by_id(node.get_id())
                return self.is_acyclic_inner()

    def is_acyclic(self):
        """
        Tests if a graph is acyclic

        Returns:
            True - if the graph is acyclic
            False - in the other case
        """
        g = copy.deepcopy(self)
        return g.is_acyclic_inner()

    def is_cyclic(self):
        """
        Tests if a graph is cyclic
        """
        return not self.is_acyclic()
    
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


    

