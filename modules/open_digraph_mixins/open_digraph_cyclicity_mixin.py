from modules.node import node
import copy

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphCyclicityMixin(object):
    def is_acyclic_inner(self: T):
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

    def is_acyclic(self: T):
        """
        Tests if a graph is acyclic

        Returns:
            True - if the graph is acyclic
            False - in the other case
        """

        g = copy.deepcopy(self)
        return g.is_acyclic_inner()

    def is_cyclic(self: T):
        """
        Tests if a graph is cyclic
        """
        return not self.is_acyclic()
