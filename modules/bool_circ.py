import copy
import random
import math

import CONFIG
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
    
    def constant_copy_transform(self, copy_id: int) -> None:
        """
        If node `copy_id` is a copy‐gate whose single parent is a constant
        ('0' or '1'), replace:
        const -> copy ->child
                       ->child
        with: const -> child
            const -> child
        
        Args:
            copy_id(int) - id of the copy node
        """
        # must be a copy node
        if copy_id not in self.get_nodes_ids(): 
            return
        copy_node = self.get_id_node_map()[copy_id]
        if copy_node.get_label() != "": 
            return

        #must have exactly one parent which is a constant
        parents = list(copy_node.get_parents().items())
        if len(parents) != 1: 
            return
        const_id, _ = parents[0]
        const_node = self.get_id_node_map().get(const_id)
        if const_node is None or const_node.get_label() not in ("0", "1"):
            return

        # constant must have only that one child
        if const_node.outdegree() != 1:
            return
        
        # if copy has no children, nothing to do
        if copy_node.outdegree() == 0:
            return

        # for each outgoing edge (copy → child), create a fresh constant
        for child_id, multiplicity in list(copy_node.get_children().items()):
            new_c = self.add_node(label=const_node.get_label())
            for _ in range(multiplicity):
                self.add_edge(new_c, child_id)

        # remove the copy (and its const→copy edge)
        self.remove_node_by_id(copy_id)

        # if the original const is now isolated, remove it too
        if const_node.indegree() == 0 and const_node.outdegree() == 0:
            self.remove_node_by_id(const_id)
        
    def constant_not_transform(self: T, not_id: int) -> None:
        """
        If node is a node_not and his parent is a const then we replace:
            const -> not -> x
        with:
            const' -> x
        Args:
            not_id(int) - id of the not node
        """
        # if not a not
        if self.get_id_node_map()[not_id].get_label() != "~":
            return

        # Grab the single parent (the constant) and the single child.
        const_id = next(iter(self[not_id].get_parents().keys()))
        child_id = next(iter(self[not_id].get_children().keys()))

        const_label = self.get_id_node_map()[const_id].get_label()
        # If it's not a constant, nothing to do.
        if const_label not in ("0", "1"):
            return

        # Build the inverted constant
        inverted = "1" if const_label == "0" else "0"
        new_const = self.add_node(label=inverted)
        self.add_edge(new_const, child_id)

        # Remove the NOT gate (and its incoming/outgoing wires)
        self.remove_node_by_id(not_id)

        # Optionally, if the original const is now orphaned, delete it
        cn = self.get_id_node_map().get(const_id)
        if cn and cn.indegree() + cn.outdegree() == 0:
            self.remove_node_by_id(const_id)

    def transform_and_zero(self, and_id: int) -> None:
        """
        If node is a node_and and his parent is a const then we replace:
            if const == 0:
                const -> and -> x
                ...   -> 
                ...   -> 
                with:
                const -> x       ... -> ''    ... -> ''
        Args:
            and_id(int) - id of the and node
        """
        # must exist and be an AND
        if and_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[and_id]
        if gate.get_label() != "&":
            return

        # find one zero‐parent (else skip)
        zero_parents = [
            p for p in gate.get_parents()
            if self.get_id_node_map()[p].get_label() == "0"
        ]
        if not zero_parents:
            return
        zero_id = zero_parents[0]

        # for every *other* parent, detach it and give it a copy node
        for p, mult in list(gate.get_parents().items()):
            if p == zero_id:
                continue
            self.remove_parallel_edges(p, and_id)
            cp = self.add_node(label="")
            self.add_edge(p, cp)

        child_id, _ = next(iter(gate.get_children().items()))
        self.add_edge(zero_id, child_id)

        #delete the AND 
        self.remove_node_by_id(and_id)


    def transform_and_one(self, and_id: int) -> None:
        """
        If node is a node_and and his parent is a const then we replace:
            if const == 1:
                const -> and -> x
                ...   -> 
                ...   -> 
                with:
                ...   -> and -> x
                ...   ->
        Args:
            and_id(int) - id of the and node
        """
        # must be an and
        if and_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[and_id]
        if gate.get_label() != "&":
            return
        to_prune: list[int] = []
        for pid, mult in list(gate.get_parents().items()):
            if self.get_id_node_map()[pid].get_label() == "1":
                self.remove_parallel_edges(pid, and_id)
                to_prune.append(pid)
        # delete isolated parent
        for pid in to_prune:
            cn = self.get_id_node_map().get(pid)
            if cn and (cn.indegree() + cn.outdegree()) == 0:
                self.remove_node_by_id(pid)

    def transform_or_zero(self, or_id: int) -> None:
        """
        Remove any '0' inputs from OR:
        (This is the mirror of transform_and_one.)
        Args:
            or_id(int) - id of the or node
        """
        if or_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[or_id]
        if gate.get_label() != "|":
            return

        
        for p in list(gate.get_parents().keys()):
            if self.get_id_node_map()[p].get_label() == "0":
                self.remove_parallel_edges(p, or_id)
                cn = self.get_id_node_map().get(p)
                if cn and (cn.indegree() + cn.outdegree()) == 0:
                    self.remove_node_by_id(p)

    def transform_or_one(self, or_id: int) -> None:
        """
        Symetric to AND with const '0'
        Args:
            or_id(int) - id of the or node
        """
        if or_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[or_id]
        if gate.get_label() != "|":
            return

        # find a '1' parent
        one_parents = [
            p for p in gate.get_parents()
            if self.get_id_node_map()[p].get_label() == "1"
        ]
        if not one_parents:
            return
        one_id = one_parents[0]

        # for every other parent, detach it and give it a copy node
        for p, _ in list(gate.get_parents().items()):
            if p == one_id:
                continue
            self.remove_parallel_edges(p, or_id)
            cp = self.add_node(label="")
            self.add_edge(p, cp)

        # OR has exactly one child in a well-formed circuit
        child_id, _ = next(iter(gate.get_children().items()))
        # rewire 1 → child
        self.add_edge(one_id, child_id)

        # delete the OR 
        self.remove_node_by_id(or_id)
    
    def transform_xor_zero(self, xor_id: int) -> None:
        """
        Remove any '0' inputs from XOR:
        (Same as for OR)
        Args:
            xor_id(int) - id of the xor node
        """
        if xor_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[xor_id]
        if gate.get_label() != "^":
            return

        for p in list(gate.get_parents().keys()):
            if self.get_id_node_map()[p].get_label() == "0":
                self.remove_parallel_edges(p, xor_id)
                zp = self.get_id_node_map().get(p)
                if zp and (zp.indegree() + zp.outdegree()) == 0:
                    self.remove_node_by_id(p)

    def transform_xor_one(self, xor_id: int) -> None:
        """
        Remove '1' inputs from XOR and add not:
              '1' -> xor -> x
              ...   ->
              ...   ->
        with:
              ...   -> not -> x
              ...   ->
        Args:
            xor_id(int) - id of the xor node
    
        """
        if xor_id not in self.get_nodes_ids():
            return
        gate = self.get_id_node_map()[xor_id]
        if gate.get_label() != "^":
            return

        # Find one '1' parent
        ones = [
            p for p in gate.get_parents().keys()
            if self.get_id_node_map()[p].get_label() == "1"
        ]
        if not ones:  # No '1' parents
            return

        # Process only one '1' parent at a time
        one_id = ones[0]  # Take the first '1' parent

        # Remove edge from '1' to XOR
        self.remove_parallel_edges(one_id, xor_id)

        # Delete '1' constant if now isolated
        node_p = self.get_id_node_map().get(one_id)
        if node_p and (node_p.indegree() + node_p.outdegree()) == 0:
            self.remove_node_by_id(one_id)

        # Get child of XOR gate
        child_id, mult = next(iter(gate.get_children().items()))

        # Add a NOT gate between XOR and its child
        self.remove_parallel_edges(xor_id, child_id)
        not_id = self.add_node(label="~")
        self.add_edge(xor_id, not_id)
        self.add_edge(not_id, child_id)

    def transform_in_zero(self, node_id: int) -> None:
        """
        Transform any '|' or '^' with no inputs to '0':
        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() not in ["|", "^"]:
            return

        # Check if the gate has no inputs
        if gate.indegree() == 0:
            # Create a '0' constant
            zero_node = self.add_node(label="0")
            for child_id, mult in list(gate.get_children().items()):
                self.remove_parallel_edges(node_id, child_id)
                # Add edges from the '0' constant to the children
                for _ in range(mult):
                    self.add_edge(zero_node, child_id)

            # Remove the original gate
            self.remove_node_by_id(node_id)

    def transform_in_one(self: T, node_id: int) -> None:
        """
        Transform any '&' with no inputs to '1':
        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != "&":
            return
        
        # Check if the gate has no inputs
        if gate.indegree() == 0:
            # Create a '1' constant
            one_node = self.add_node(label="1")
            for child_id, mult in list(gate.get_children().items()):
                self.remove_parallel_edges(node_id, child_id)
                # Add edges from the '1' constant to the children
                for _ in range(mult):
                    self.add_edge(one_node, child_id)
            # Remove the original gate
            self.remove_node_by_id(node_id)

    # encoder new rules
    # ======
    def transform_associative_xor(self: T, node_id: int) -> None:
        """
        Transform two connected xors to one xor with the parents of both

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '^':
            return
        parents = list(gate.get_parents().keys())
        if len(parents) == 0:
            return

        def is_node_id_corresponds_to_xor_gate(nid: int) -> bool:
            if nid not in self.get_nodes_ids():
                return False
            return self.get_id_node_map()[nid].get_label() == '^'

        xor_parents = [par_id for par_id in parents if is_node_id_corresponds_to_xor_gate(par_id)]
        while len(xor_parents) != 0:
            xor_par_id = xor_parents[0]
            xor_parents.remove(xor_par_id)

            self.fuse_nodes(node_id, xor_par_id)

    def transform_associative_copy(self: T, node_id: int) -> None:
        """
        Transform two connected copies to one copy with the parents of both

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return
        if node_id in self.get_outputs_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '':
            return
        parents = list(gate.get_parents().keys())
        if len(parents) != 1: # cause copy can have ONLY ONE parent
            return

        par_node_id = parents[0]
        par_node = self.get_id_node_map()[par_node_id]

        if par_node.get_label() != '': # the parent must be copy
            return

        self.fuse_nodes(par_node_id, node_id)

    def transform_involution_xor(self: T, node_id: int) -> None:
        """
        If the given `xor` node has a copy parent than it leaves only one edge if the multiplicity is odd, or remove all the edges between those nodes if the multiplicity is even

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '^':
            return

        parents = list(gate.get_parents().keys())
        if len(parents) == 0:
            return

        def is_node_id_corresponds_to_copy_mult_two_gate(nid: int) -> bool:
            if nid not in self.get_nodes_ids() or nid not in parents:
                return False
            return self.get_id_node_map()[nid].get_label() == '' and gate.get_parents()[nid] > 1

        copy_parents = [par_id for par_id in parents if is_node_id_corresponds_to_copy_mult_two_gate(par_id)]
        while len(copy_parents) != 0:
            copy_par_id = copy_parents[0]
            multiplicity = gate.get_parents()[copy_par_id]
            num_of_edges_to_leave = multiplicity % 2 # if number is odd we leave 1 edge, if even, we remove all the edges
            copy_parents.remove(copy_par_id)
            self.remove_parallel_edges(copy_par_id, node_id)
            if num_of_edges_to_leave == 1:
                self.add_edge(copy_par_id, node_id)

    def transform_erase_operator(self: T, node_id: int) -> None:
        """
        If the given copy node has outdegree 0 (i.e doesn't have children) but has the in degree at least 1
        (especially if it's an operator) than it'll remove the operator and connect all it's parents to the created dead-end copy nodes.

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return
        if node_id in self.get_outputs_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '':
            return

        parents = list(gate.get_parents().keys())
        if len(parents) != 1:
            return

        if len(list(gate.get_children().keys())) != 0:
            return

        parent_id = parents[0]
        parent_node = self[parent_id]

        match parent_node.get_label():
            case '':
                return
            case '0' | '1':
                if len(list(parent_node.get_children().keys())) > 1: # if the constant has many children, then our copy doesn't have any sense, remove it
                    self.remove_node_by_id(node_id)
                elif len(list(parent_node.get_children().keys())) == 1: # our node is the only child of the constant
                    self.remove_node_by_id(node_id)
                    self.remove_node_by_id(parent_id)
            case _:
                parents_id_of_par_node = list(parent_node.get_parents().keys())
                for par_id in parents_id_of_par_node:
                    new_copy_node_id = self.add_node('')
                    for _ in range(parent_node.get_parents()[par_id]):
                        self.add_edge(par_id, new_copy_node_id)
                self.remove_node_by_id(parent_id)
                self.remove_node_by_id(node_id)

    def transform_xor_if_has_parent_not(self: T, node_id: int) -> None:
        """
        If encounters `not` gate in the parents of the given `xor` gate, then it removes the `not`
        gate from parents and adds as a child 

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '^':
            return
        parents = list(gate.get_parents().keys())
        if len(parents) == 0:
            return

        def is_node_id_corresponds_to_not_gate(nid: int) -> bool:
            if nid not in self.get_nodes_ids():
                return False
            return self.get_id_node_map()[nid].get_label() == '~'

        not_parents = [par_id for par_id in parents if is_node_id_corresponds_to_not_gate(par_id)]
        while len(not_parents) != 0:
            not_par_id = not_parents[0]
            not_parents.remove(not_par_id)
            
            par_of_not_id = next(iter(self[not_par_id].get_parents().keys()))

            self.add_edge(par_of_not_id, node_id)

            self.remove_node_by_id(not_par_id)

            
            child_id = next(iter(gate.get_children().keys()))
            self.remove_parallel_edges(node_id, child_id)

            new_not_id = self.add_node('~')
            self.add_edge(node_id, new_not_id)
            self.add_edge(new_not_id, child_id)
    def transform_copy_if_has_parent_not(self: T, node_id: int) -> None:
        """
        If encounters `not` gate in the parents of the given `copy` gate, then it removes the `not`
        gate from parents and adds as a child 

        Args:
            node_id(int) - id of the node
        """
        if node_id not in self.get_nodes_ids():
            return

        gate = self.get_id_node_map()[node_id]
        if gate.get_label() != '':
            return
        parents = list(gate.get_parents().keys())
        if len(parents) == 0:
            return

        def is_node_id_corresponds_to_not_gate(nid: int) -> bool:
            if nid not in self.get_nodes_ids():
                return False
            return self.get_id_node_map()[nid].get_label() == '~'

        parent_id = next(iter(gate.get_parents().keys()))
        parent_node = self[parent_id]
        if parent_node.get_label() != '~':
            return

        children = list(gate.get_children().keys())
        if len(children) == 0:
            return
        par_of_par_id = next(iter(parent_node.get_parents().keys()))
        self.fuse_nodes(par_of_par_id, parent_id)
        for child_id in children:
            mult = gate.get_children()[child_id]
            for _ in range(mult):
                new_not_id = self.add_node('~')
                self.add_edge(node_id, new_not_id)
                self.add_edge(new_not_id, child_id)
            self.remove_parallel_edges(node_id, child_id)
    def transform_not_involution(self: T, node_id: int) -> None:
        """
        If the given `not` gate has a `not` parent then we remove both nodes and connect parent and child cause (~~ = identity)

        Args:
            node_id(int) - if of the node
        """
        if node_id not in self.get_nodes_ids():
            return
        gate: node = self[node_id]
        if gate.get_label() != '~':
            return
        if gate.indegree() != 1 or gate.outdegree() != 1:
            return

        parent_id = next(iter(gate.get_parents().keys()))
        parent_node: node = self[parent_id]

        if parent_node.get_label() != '~':
            return
        if parent_node.indegree() != 1 or parent_node.outdegree() != 1:
            return

        par_conn_id = next(iter(parent_node.get_parents().keys()))
        ch_conn_id = next(iter(gate.get_children().keys()))
        self.add_edge(par_conn_id, ch_conn_id)

        self.remove_node_by_id(node_id)
        self.remove_node_by_id(parent_id)
    # ======

    def evaluate(self) -> None:
        """
        Apply all transformation rules to simplify a bool circuit until 
        no more transformations are applicable.

        """
        changed = True
        debug_id = 0
        while changed:
            changed = False

            # Current nodes
            node_ids = list(self.get_nodes_ids())

            # Apply transformations to each node
            for node_id in node_ids:
                if node_id not in self.get_nodes_ids():  # Node might have been removed by previous transformation
                    continue
                
                node = self.get_id_node_map().get(node_id)
                if not node:
                    continue

                # Store state before transformation
                old_nodes_count = len(self.get_nodes_ids())

                # Apply transformations based on node type
                label = node.get_label()

                if label == '':  # Copy
                    self.constant_copy_transform(node_id)
                    self.transform_copy_if_has_parent_not(node_id)
                    self.transform_associative_copy(node_id)
                    self.transform_erase_operator(node_id)
                elif label == '~':  # NOT
                    self.constant_not_transform(node_id)
                    self.transform_not_involution(node_id)
                elif label == '&':  # AND
                    self.transform_and_zero(node_id)
                    self.transform_and_one(node_id)
                    self.transform_in_one(node_id)
                elif label == '|':  # OR
                    self.transform_or_zero(node_id)
                    self.transform_or_one(node_id)
                    self.transform_in_zero(node_id)
                elif label == '^':  # XOR gate
                    self.transform_xor_zero(node_id)
                    self.transform_xor_one(node_id)
                    self.transform_in_zero(node_id)
                    self.transform_associative_xor(node_id)
                    self.transform_involution_xor(node_id)
                    self.transform_xor_if_has_parent_not(node_id)

                # Check if any transformation was applied
                if old_nodes_count != len(self.get_nodes_ids()) or node_id not in self.get_nodes_ids():
                    changed = True
                    if CONFIG.DEBUG:
                        self.save_as_pdf_file(f"decoder_encoder_{debug_id}")
                        logger.trace(f"decoder_encoder{debug_id}")
                        debug_id += 1
                    break  # Start from the beginning

                
                

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
                logger.trace(f"{node_id} | {in_d} {out_d}")

        return bool_circ(graph)
        # return graph
    @classmethod
    def build_adder(cls: Type[TB], n: int, reg1: list[str], reg2: list[str], carry: str) -> 'bool_circ':
        """
        Recursively constructs a binary adder circuit of size 2^n using two input registers and an initial carry.

        Args:
            n (int): The exponent such that each register has 2^n bits.
            reg1 (list[str]): The first binary register as a list of string labels.
            reg2 (list[str]): The second binary register as a list of string labels.
            carry (str): The label for the initial carry input to the most significant bit.

        Constraints: 
            - n >= 0
            - len(reg1) == len(reg2)
            - len(reg1) == 2^n

        Returns:
            bool_circ: A boolean circuit representing the binary addition of `reg1` and `reg2`
                       with an initial carry, constructed as a composed logic graph.
        """

        vars1 = [f'x{i}' for i in range(len(reg1))]
        vars2 = [f'y{i}' for i in range(len(reg2))]

        var_to_num = {}
        for i in range(len(vars1)):
            var_to_num[vars1[i]] = reg1[i]

        for i in range(len(vars2)):
            var_to_num[vars2[i]] = reg2[i]

        var_to_num["c1"] = carry
        res = cls.build_adder_inner(n, vars1, vars2, "c1")

        for node_id in res.get_inputs_ids():
            if res[node_id].label in ("0", "1"):
                continue
            res[node_id].label = var_to_num[ res[node_id].label ]

        return res

    @classmethod
    def build_adder_inner(cls: Type[TB], n: int, reg1: list[str], reg2: list[str], carry: str) -> 'bool_circ':
        """
        This is an inner (helper) build_adder function that implements the method. 

        !!! In build_adder we create two arrays of strings with distinct names in order to simulate different variables, 
        !!! then we pass it to this build_adder_inner where we construct the bool_circ, and then we replace input labels of the disctinct 
        !!! generated variables with their real passed values.

        Recursively constructs a binary adder circuit of size 2^n using two input registers and an initial carry.

        Args:
            n (int): The exponent such that each register has 2^n bits.
            reg1 (list[str]): The first binary register as a list of string labels.
            reg2 (list[str]): The second binary register as a list of string labels.
            carry (str): The label for the initial carry input to the most significant bit.

        Constraints: 
            - n >= 0
            - len(reg1) == len(reg2)
            - len(reg1) == 2^n

        Returns:
            bool_circ: A boolean circuit representing the binary addition of `reg1` and `reg2`
                       with an initial carry, constructed as a composed logic graph.
        """

        # how it works note:
        #         This function splits the registers into halves and recursively builds two smaller adders:
        # one for the lower bits (with carry = '0') and one for the upper bits (with the given carry).
        # It then merges them into a single circuit and connects them accordingly.
        assert n >= 0
        assert len(reg1) == len(reg2)
        assert len(reg1) == (2**n)

        if n == 0:
            return build_adder_0(reg1, reg2, carry)

        sub_num = 2**(n-1) # the size of the register for Additioner (n-1)

        # dividing registers on two so we can pass them to the Additioners (n-1)
        reg_1_2 = reg1[sub_num:]
        reg_1_1 = reg1[0:sub_num] 

        reg_2_1 = reg2[0:sub_num]
        reg_2_2 = reg2[sub_num:]

        # passing divided registers to the Additioners (n-1)
        circ1 = cls.build_adder_inner(n-1, reg_1_1, reg_2_1, '0')
        circ2 = cls.build_adder_inner(n-1, reg_1_2, reg_2_2, carry)
        
        
        # getting lengths of the additioners (n-1) se we can rearrange inputs and outputs of the resulting additioner (boolean circuit)
        inputs_1 = circ1.get_inputs_ids()
        old_output_num = len(circ1.get_outputs_ids())
        old_input_num = len(inputs_1)

        new_bool_circ = circ1.parallel(circ2)

        # removing one output (cause of 2 additioners)
        # and passing the resulted carry of the right additioner (n-1) to the left one
        output_of_second_add_n = new_bool_circ.get_outputs_ids()[old_output_num]
        output_parent = list(new_bool_circ.get_id_node_map()[output_of_second_add_n].parents.keys())[0]
        new_bool_circ.remove_node_by_id(output_of_second_add_n)

        last_input_of_first_add_n = new_bool_circ.get_inputs_ids()[old_input_num-1]
        input_child = list(new_bool_circ.get_id_node_map()[last_input_of_first_add_n].children.keys())[0]
        new_bool_circ.remove_node_by_id(last_input_of_first_add_n)
        new_bool_circ.add_edge(output_parent, input_child)

        return bool_circ(new_bool_circ) # temp return

    @classmethod
    def from_number(cls: Type[TB], number: int, size: int = 8) -> 'bool_circ':
        """
        Returns a boolean circuit from the given number and the register size

        Args:
            number(int) - the number to code to the circuit
            size(int) - size of the register
        Returns:
            bool_circ
        """
        res = open_digraph.identity(size)
        bin_rep = bin(number)[2:]
        rev_bin_rep = list(reversed(list(bin_rep)))
        assert len(bin_rep) <= size

        for idx, input_id in enumerate(reversed(res.get_inputs_ids())):
            if idx >= len(bin_rep):
                res[input_id].label = '0' 
            else:
                res[input_id].label = rev_bin_rep[idx]
        return bool_circ(res)

    @classmethod
    def build_half_adder(cls: Type[TB], n: int, reg1: list[str], reg2: list[str]) -> 'bool_circ':
        """
        Recursively constructs a binary half adder circuit of size 2^n using two input registers and an initial carry.

        Args:
            n (int): The exponent such that each register has 2^n bits.
            reg1 (list[str]): The first binary register as a list of string labels.
            reg2 (list[str]): The second binary register as a list of string labels.

        Constraints: 
            - n >= 0
            - len(reg1) == len(reg2)
            - len(reg1) == 2^n

        Returns:
            bool_circ: A boolean circuit representing the binary addition of `reg1` and `reg2`
                       with an initial carry, constructed as a composed logic graph.
        """

        return cls.build_adder(n, reg1, reg2, '0')

    @classmethod
    def carry_lookahead_4(cls: Type[TB], reg1: list[str], reg2: list[str], c0: str) -> 'bool_circ':
        """
        Constructs a 4-bit adder using ripple-carry logic.
        Uses dedicated input port nodes and ensures output port nodes have empty labels.

        Args:
            reg1 (list[str]): The first binary register (4 bits, MSB first e.g., [A3, A2, A1, A0]).
            reg2 (list[str]): The second binary register (4 bits, MSB first e.g., [B3, B2, B1, B0]).
            c0 (str): The label for the initial carry input (for the LSB stage).

        Returns:
            bool_circ: A boolean circuit representing the 4-bit addition.
        """
        assert len(reg1) == 4 and len(reg2) == 4, "Registers must be 4 bits long."

        g = open_digraph.empty()

        # Helper to create a binary gate and connect inputs
        def create_binary_gate_with_connections(id_a, id_b, gate_label):
            gate_node_id = g.add_node(label=gate_label)
            g.add_edge(id_a, gate_node_id)
            g.add_edge(id_b, gate_node_id)
            return gate_node_id

        
        a_val_nodes_msb_first = []
        for i in range(4): 
            bit_label = reg1[i]
            val_node_id = g.add_node(label='')
            g.add_input_node(val_node_id, label=bit_label) 
            a_val_nodes_msb_first.append(val_node_id)

        b_val_nodes_msb_first = []
        for i in range(4): 
            bit_label = reg2[i]
            val_node_id = g.add_node(label='')
            g.add_input_node(val_node_id, label=bit_label)
            b_val_nodes_msb_first.append(val_node_id)

        c0_val_node_id = g.add_node(label='')
        g.add_input_node(c0_val_node_id, label=c0)


        a_val_nodes_lsb_first = a_val_nodes_msb_first[::-1] 
        b_val_nodes_lsb_first = b_val_nodes_msb_first[::-1] 

        propagate_copy_nodes_lsb_first = [] 
        generate_gate_nodes_lsb_first = []   

        for i in range(4): 
            a_i_val_node = a_val_nodes_lsb_first[i]
            b_i_val_node = b_val_nodes_lsb_first[i]
            
            generate_gate_nodes_lsb_first.append(
                create_binary_gate_with_connections(a_i_val_node, b_i_val_node, '&')
            )
            
            p_i_xor_gate_node = create_binary_gate_with_connections(a_i_val_node, b_i_val_node, '^')
            
            copy_p_i_node = g.add_node(label='') 
            g.add_edge(p_i_xor_gate_node, copy_p_i_node)
            propagate_copy_nodes_lsb_first.append(copy_p_i_node)

        
        current_carry_val_node = c0_val_node_id 
        
        carry_logic_nodes_for_sum_and_next_stage = [current_carry_val_node]


        for i in range(4): 
            p_i_copy_node = propagate_copy_nodes_lsb_first[i] 
            g_i_gate_node = generate_gate_nodes_lsb_first[i]  
            c_in_i_logic_node = carry_logic_nodes_for_sum_and_next_stage[i] 

            p_and_c_gate_node = create_binary_gate_with_connections(p_i_copy_node, c_in_i_logic_node, '&')
            c_out_i_or_gate_node = create_binary_gate_with_connections(g_i_gate_node, p_and_c_gate_node, '|')
            
            copy_c_out_i_node = g.add_node(label='')
            g.add_edge(c_out_i_or_gate_node, copy_c_out_i_node)
            carry_logic_nodes_for_sum_and_next_stage.append(copy_c_out_i_node) 

        sum_gate_nodes_lsb_first = []
        for i in range(4): 
            p_i_copy_node = propagate_copy_nodes_lsb_first[i]
            c_in_i_logic_node = carry_logic_nodes_for_sum_and_next_stage[i] 
            
            sum_gate_node = create_binary_gate_with_connections(p_i_copy_node, c_in_i_logic_node, '^')
            sum_gate_nodes_lsb_first.append(sum_gate_node) # Stores [S0_gate, S1_gate, S2_gate, S3_gate]
        
        final_carry_out_logic_node = carry_logic_nodes_for_sum_and_next_stage[4]
        g.add_output_node(final_carry_out_logic_node, label="") 

        sum_gate_nodes_msb_first = sum_gate_nodes_lsb_first[::-1]
        for i in range(4): 
            g.add_output_node(sum_gate_nodes_msb_first[i], label="") 
            
        return bool_circ(g)
    
    @classmethod
    def generate_4bit_encoder(cls: Type[TB], bit1: str, bit2: str, bit3: str, bit4: str) -> 'bool_circ':
        """
        Generates 4bit encoder boolean circuit

        Args:
            bit1(str) - first bit
            bit2(str) - second bit
            bit3(str) - third bit
            bit4(str) - fourth bit
        Returns:
            boolean circuit with 7 outputs
        """
        old_bit1, old_bit2, old_bit3, old_bit4 = bit1, bit2, bit3, bit4
        bit1, bit2, bit3, bit4 = "x1", "x2", "x3", "x4",
        rename_dict = {bit1:old_bit1, bit2:old_bit2, bit3:old_bit3, bit4:old_bit4}
        output_1 = f"(({bit1})^({bit2})^({bit4}))"
        output_2 = f"(({bit1})^({bit3})^({bit4}))"
        output_3 = f"({bit1})"
        output_4 = f"(({bit2})^({bit3})^({bit4}))"
        output_5 = f"({bit2})"
        output_6 = f"({bit3})"
        output_7 = f"({bit4})"

        res_g = parse_parentheses(output_1, output_2, output_3, output_4, output_5, output_6, output_7)[0]
        for input_id in res_g.get_inputs_ids():
            res_g[input_id].label = rename_dict[res_g[input_id].label]
        return res_g

    @classmethod
    def generate_4bit_decoder(cls: Type[TB], bit1: str, bit2: str, bit3: str, bit4: str, bit5: str, bit6: str, bit7: str) -> 'bool_circ':
        """
        Generates 4bit decoder boolean circuit

        Args:
            bit1(str) - first bit
            bit2(str) - second bit
            bit3(str) - third bit
            bit4(str) - fourth bit
            bit5(str) - fifth bit
            bit6(str) - sixth bit
            bit7(str) - seventh bit
        Returns:
            boolean circuit with 4 outputs
        """
        old_bit1, old_bit2, old_bit3, old_bit4, old_bit5, old_bit6, old_bit7 = bit1, bit2, bit3, bit4, bit5, bit6, bit7
        bit1, bit2, bit3, bit4, bit5, bit6, bit7 = "x1", "x2", "x3", "x4", "x5", "x6", "x7"
        rename_dict = {bit1:old_bit1, bit2:old_bit2, bit3:old_bit3, bit4:old_bit4, bit5:old_bit5, bit6:old_bit6, bit7:old_bit7}
        # f_l = first_line
        xor_f_l_1 = f"(({bit1})^({bit3})^({bit5})^({bit7}))"
        xor_f_l_2 = f"(({bit2})^({bit3})^({bit6})^({bit7}))"
        xor_f_l_3 = f"(({bit4})^({bit5})^({bit6})^({bit7}))"

        output_1 = f"((({xor_f_l_1})&({xor_f_l_2})&(~{xor_f_l_3}))^({bit3}))"
        output_2 = f"((({xor_f_l_1})&(~{xor_f_l_2})&({xor_f_l_3}))^({bit5}))"
        output_3 = f"(((~{xor_f_l_1})&({xor_f_l_2})&({xor_f_l_3}))^({bit6}))"
        output_4 = f"((({xor_f_l_1})&({xor_f_l_2})&({xor_f_l_3}))^({bit7}))"

        res_g = parse_parentheses(output_1, output_2, output_3, output_4)[0]
        for input_id in res_g.get_inputs_ids():
            res_g[input_id].label = rename_dict[res_g[input_id].label]
        curr_input_ids = res_g.get_inputs_ids()
        corr_input_ids = [curr_input_ids[0], curr_input_ids[4], curr_input_ids[1], curr_input_ids[6], curr_input_ids[2], curr_input_ids[5], curr_input_ids[3]]
        res_g.set_inputs(corr_input_ids)
        return res_g

    @classmethod 
    def carry_lookahead_4n(cls: Type[TB],
                           reg1: list[str],
                           reg2: list[str],
                           carry: str) -> 'bool_circ':
        """
        Chains 4‑bit carry‑lookahead blocks to handle any
        multiple of 4 bits by passing each block’s carry‑out
        into the next block’s carry‑in.
        """
        assert len(reg1) == len(reg2) and len(reg1) % 4 == 0
        blocks = len(reg1) // 4

        if len(reg1) == 4:
            return cls.carry_lookahead_4(reg1, reg2, carry)
        sub_len = len(reg1) - 4


        reg_1_2 = reg1[0:4]
        reg_1_1 = reg1[4:] 

        reg_2_1 = reg2[0:4]
        reg_2_2 = reg2[4:]

        circ1 = cls.carry_lookahead_4(reg_1_1, reg_2_1, 'carry_temp')
        circ2 = cls.carry_lookahead_4n(reg_1_2, reg_2_2, carry)
        
        
        inputs_1 = circ1.get_inputs_ids()
        smaller_output_num = len(circ1.get_outputs_ids())
        smaller_input_num = len(circ1.get_inputs_ids())

        bigger_output_num = len(circ2.get_outputs_ids())
        bigger_input_num = len(circ2.get_inputs_ids())

        old_output_num = len(circ1.get_outputs_ids())
        old_input_num = len(inputs_1)

        new_bool_circ = circ1.parallel(circ2)

        # removing one output (cause of 2 additioners)
        # and passing the resulted carry of the right additioner (4n-4) to the left one
        output_of_second_add_n = new_bool_circ.get_outputs_ids()[smaller_output_num]
        output_parent = list(new_bool_circ.get_id_node_map()[output_of_second_add_n].parents.keys())[0]
        new_bool_circ.remove_node_by_id(output_of_second_add_n)

        last_input_of_first_add_n = new_bool_circ.get_inputs_ids()[smaller_input_num-1]
        input_child = list(new_bool_circ.get_id_node_map()[last_input_of_first_add_n].children.keys())[0]
        new_bool_circ.remove_node_by_id(last_input_of_first_add_n)
        new_bool_circ.add_edge(output_parent, input_child)

        first_small_part_of_inputs = new_bool_circ.get_inputs_ids()[0:4]
        second_small_part_of_inputs = new_bool_circ.get_inputs_ids()[4:8]

        first_big_part_of_inputs = new_bool_circ.get_inputs_ids()[8:sub_len+8]
        second_big_part_of_inputs = new_bool_circ.get_inputs_ids()[sub_len+8:-1]
        last_carry = new_bool_circ.get_inputs_ids()[-1]

        res_inputs = []
        for i in first_small_part_of_inputs:
            res_inputs.append(i)
        for i in first_big_part_of_inputs:
            res_inputs.append(i)
        for i in second_small_part_of_inputs:
            res_inputs.append(i)
        for i in second_big_part_of_inputs:
            res_inputs.append(i)
        res_inputs.append(last_carry)
        new_bool_circ.set_inputs(res_inputs)
        

        return bool_circ(new_bool_circ) 

def build_adder_0(reg1: list[str], reg2: list[str], carry: str) -> 'bool_circ':
    """
    Builds a boolean circuit representing an additioner of two bits

    Args:
        reg1(list[str]) - first variable in a list
        reg2(list[str]) - second variable in a list
        carry(str) - carry

    
    Returns:
        bool_circ
    """
    assert len(reg1) ==1 
    assert len(reg2) ==1 

    for i in range(len(reg1)):
        reg1[i] = str(reg1[i])

    for i in range(len(reg2)):
        reg2[i] = str(reg2[i])

    reg = [reg1[0], reg2[0]]
    res, vars = parse_parentheses(f"((({reg[0]})&({reg[1]}))|((({reg[0]})^({reg[1]}))&({carry})))", f"((({reg[0]})^({reg[1]}))^({carry}))")
    return res


def parse_parentheses(*args) -> tuple[bool_circ, list[str]]:
    """
    Parses string to a boolean circuit    

    Args:
        args - list of string to parse to a boolean circuit

    Returns:
        bool_circ, list[str] - names of the input variables
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
    
    # return g, var_names
    return bool_circ(g), var_names

def add_two_numbers(num1: int, num2: int) -> int:
    biggest = num1 if num1 > num2 else num2 # get the biggest num

    power = math.ceil(math.log2(biggest)) # get it's closest power of two 
    two_power = 2**power


    num_1_bc = bool_circ.from_number(num1, two_power) # construct number's circuit
    num_2_bc = bool_circ.from_number(num2, two_power)

    num_1_arr = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids()] # get it's binary representation
    num_2_arr = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids()]

    bc = bool_circ.build_half_adder(power, num_1_arr, num_2_arr) # construct the circuit
    bc.evaluate() # evaluate the circuit

    bin_res = get_result_of_evaluated_additioner(bc) # get the reuslt
    return int(bin_res, 2) # convert to int

def get_result_of_evaluated_additioner(bc: 'bool_circ') -> str:
    """
    Gets an evaluated boolean circuit additioner and extracts the calculated result in the form of string

    Args:
        bc(bool_circ) - evaluated boolean circuit
    Returns:
        str - the result
    """

    output_nodes = [ n for n in bc.get_nodes_by_ids(bc.get_outputs_ids())] # get all output nodes
    par_out_nodes = [ bc.get_id_node_map()[ list(n.get_parents().keys())[0] ] for n in output_nodes] # get their parents

    labels_for_par_nodes = [n.get_label() for n in par_out_nodes] # get labels of the last ones
    list_res = labels_for_par_nodes[1:] # remove the carry
    res_str = "".join(list_res) # convert to string

    return res_str

def get_result_of_evaluated_enc_dec(bc: 'bool_circ') -> str:
    """
    Gets an evaluated boolean circuit additioner and extracts the calculated result in the form of string

    Args:
        bc(bool_circ) - evaluated boolean circuit
    Returns:
        str - the result
    """

    output_nodes = [ n for n in bc.get_nodes_by_ids(bc.get_outputs_ids())] # get all output nodes
    par_out_nodes = [ bc.get_id_node_map()[ list(n.get_parents().keys())[0] ] for n in output_nodes] # get their parents

    labels_for_par_nodes = [n.get_label() for n in par_out_nodes] # get labels of the last ones
    list_res = labels_for_par_nodes[:] # remove the carry
    res_str = "".join(list_res) # convert to string

    return res_str
