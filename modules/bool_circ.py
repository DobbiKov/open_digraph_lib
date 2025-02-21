import copy
from open_digraph import node, open_digraph

class bool_circ(open_digraph):
    def __init__(self, inputs, outputs, nodes):
        super().__init__(inputs, outputs, nodes)

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
    

