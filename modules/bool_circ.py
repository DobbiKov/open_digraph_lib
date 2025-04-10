import copy
from modules.open_digraph import node, open_digraph

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class bool_circ(open_digraph):
    def __init__(self, g: open_digraph, debug: bool=False):
        """
        Constructor of boolean circuit

        Args:
            g(open_digraph)
            debug(bool) - set to True if you want to create the circuit anyway even if it is not well formed
        """
        if debug is True:
            super().__init__(g.inputs, g.outputs, list(g.nodes.values()))
            return None

        if not g.is_well_formed():
            g = open_digraph.empty()
            
        super().__init__(g.inputs, g.outputs, list(g.nodes.values()))
        if not self.is_well_formed():
            g = open_digraph.empty()
            super().__init__(g.inputs, g.outputs, list(g.nodes.values()))

    
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

            if node.get_id() in self.get_inputs_ids() or node.get_id() in self.get_outputs_ids(): # temporary
                continue

            if label == '':
                if in_d != 1:
                    return False
            elif label in ['&', '|','^']:
                if out_d != 1:
                    return False
            elif label == '~':
                if out_d != 1 or in_d != 1:
                    return False
            elif label in  ['1', '0']:
                if out_d != 0:
                    return False
            else: 
                return False
        return True


def parse_parentheses(*args) -> T:
    """
    Parses string to a open_digraph    

    Args:
        s(str) - string to parse

    Returns:
        open_digraph
    """
    g = open_digraph.empty()

    for s in args:
        n = g.add_node()
        out = g.add_output_node(n, label="")
        current_node  = n

        s2 = ''
        for char in s:
            if(char=='('):
                g[current_node].set_label(s2)
                new_node = g.add_node()
                g.add_edge(new_node, current_node)
                current_node = new_node
                s2 = ''
            elif(char==')'):
                curr_label = g[current_node].get_label()
                g[current_node].set_label(curr_label + s2)
                current_node = list(g[current_node].get_children().keys())[0]
                s2 = ''
            else:
                s2 += char

    # before = g.copy()

    # fusion same variables into one node
    id_node_map = g.get_id_node_map()
    variables = {}
    var_names = []

    for idx in g.get_nodes_ids():
        node = id_node_map[idx]
        label = node.get_label()
        if label == '' or label in ['&', '~', '|', '^']:
            continue
        if label in variables: # fusion
            main_node_idx = variables[label]
            g.fuse_nodes(main_node_idx, idx)
        else: # not seen yet, add
            var_names.append(label)
            variables[label] = idx
            g[idx].set_label('')
            g.add_input_node(idx, label)
    
    return g, var_names
