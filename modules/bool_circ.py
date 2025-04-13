import copy
import random

from loguru import logger
from modules.open_digraph import node, open_digraph

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")
TB = TypeVar("TB", bound="bool_circ")

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
                    logger.trace("copy node has more than one parent nodes, or 0")
                    return False
            elif label in ['&', '|','^']:
                if out_d != 1:
                    logger.trace("Binary operation node has more than one or 0 children nodes")
                    return False
            elif label == '~':
                if out_d != 1 or in_d != 1:
                    logger.trace("unary operation node doesn't have one and only one input and output edges")
                    return False
            elif label in  ['1', '0']:
                if in_d != 0:
                    logger.trace("numbered node has at least one in edge")
                    return False
            else: 
                logger.trace("invalid label")
                return False
        return True

    @classmethod
    def random_bool_circ_from_graph(cls: Type[TB], graph: 'open_digraph', inputs: int = 1, outputs: int = 1) -> 'bool_circ':
        """
        Generates random boolean circuit from a given graph

        Args:
            graph(open_digraph) - a graph to construct random boolean circuit from
        Optional args:
            inputs(int) - number of desired inputs (default: 1)
            outputs(int) - number of desired outputs (default: 1)
        Returns:
            bool_circ
        """
        binary_operation_signs = ['&', '|', '^']
        unary_operation_signs = ['~']


            # etape 2
        for node_id in graph.get_nodes_ids():
            node = graph.get_id_node_map()[node_id]
            par_num = len(list(node.get_parents().keys()))
            chi_num = len(list(node.get_children().keys()))
            if par_num == 0:
                graph.add_input_node(node_id)

            if chi_num == 0:
                graph.add_output_node(node_id)

            # etape 2 bis

        for node_id in graph.get_nodes_ids():
            node = graph.get_id_node_map()[node_id]
            par_num = len(list(node.get_parents().keys()))
            chi_num = len(list(node.get_children().keys()))
            # inputs
            while len(graph.get_inputs_ids()) < inputs:
                possible_node_ids = [id for id in graph.get_nodes_ids() if id not in graph.get_inputs_ids()]
                rand_id = random.randint(0, len(possible_node_ids)-1)
                graph.add_input_node(rand_id)
            while len(graph.get_inputs_ids()) > inputs:
                possible_node_ids = graph.get_inputs_ids().copy()
                random.shuffle(possible_node_ids)
                # we can access them because our inputs number is greater than 1!
                input_id_1 = possible_node_ids[0]
                input_id_2 = possible_node_ids[1]

                # nodes that inputs pointing at
                node_1 = list(graph.get_id_node_map()[input_id_1].get_children().keys())[0]
                node_2 = list(graph.get_id_node_map()[input_id_2].get_children().keys())[0]

                graph.remove_node_by_id(input_id_1)
                graph.remove_node_by_id(input_id_2)
                new_id = graph.add_node('', {}, {node_1:1, node_2:1})
                graph.add_input_node(new_id)

            # outputs
            while len(graph.get_outputs_ids()) < outputs:
                possible_node_ids = [id for id in graph.get_nodes_ids() if id not in graph.get_outputs_ids()]
                rand_id = random.randint(0, len(possible_node_ids)-1)
                graph.add_output_node(rand_id)
            while len(graph.get_outputs_ids()) > outputs:
                possible_node_ids = graph.get_outputs_ids().copy()
                random.shuffle(possible_node_ids)
                # we can access them because our inputs number is greater than 1!
                output_id_1 = possible_node_ids[0]
                output_id_2 = possible_node_ids[1]

                # nodes that outputs are pointed by 
                node_1 = list(graph.get_id_node_map()[output_id_1].get_parents().keys())[0]
                node_2 = list(graph.get_id_node_map()[output_id_2].get_parents().keys())[0]

                graph.remove_node_by_id(output_id_1)
                graph.remove_node_by_id(output_id_2)
                new_id = graph.add_node('', {node_1:1, node_2:1}, {})
                graph.add_output_node(new_id)
                

        # etape 3
        for node_id in graph.get_nodes_ids():
            node = graph.get_id_node_map()[node_id]
            in_d = node.indegree()
            out_d = node.outdegree()
            if in_d == out_d and in_d == 1:
                rand_num = random.randint(0, len(unary_operation_signs)-1)
                rand_lab = unary_operation_signs[rand_num]
                graph[node_id].set_label(rand_lab)
            elif in_d == 1 and out_d > 1:
                graph[node_id].set_label("")
            elif in_d > 1 and out_d == 1:
                rand_num = random.randint(0, len(binary_operation_signs)-1)
                rand_lab = binary_operation_signs[rand_num]
                graph[node_id].set_label(rand_lab)
            elif in_d > 1 and out_d > 1:
                new_id = graph.add_node('') # making new copy node

                for ch_id, ch_mult in list(node.get_children().items()).copy():
                    graph.remove_parallel_edges(node_id, ch_id) # removing children from current node
                    for _ in range(ch_mult): # adding children to the new created copy node
                        graph.add_edge(new_id, ch_id)
                graph.add_edge(node_id, new_id) # pointing current node to the new one

                # giving binary operation label to the current node
                rand_num = random.randint(0, len(binary_operation_signs)-1) 
                rand_lab = binary_operation_signs[rand_num]
                graph[node_id].set_label(rand_lab)
            else:
                print(node_id, "| ", par_num, chi_num, in_d, out_d)

        return bool_circ(graph)
        # return graph


def parse_parentheses(*args) -> bool_circ:
    """
    Parses string to a open_digraph    

    Args:
        args - list of string to parse to a boolean circuit

    Returns:
        bool_circ
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
    
    return bool_circ(g), var_names

