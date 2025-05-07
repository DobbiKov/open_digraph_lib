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

    def evaluate(self) -> None:
        """
        Apply all transformation rules to simplify a bool circuit until 
        no more transformations are applicable.

        """
        changed = True
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
                elif label == '~':  # NOT
                    self.constant_not_transform(node_id)
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

                # Check if any transformation was applied
                if old_nodes_count != len(self.get_nodes_ids()) or node_id not in self.get_nodes_ids():
                    changed = True
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
        circ1 = cls.build_adder(n-1, reg_1_1, reg_2_1, '0')
        circ2 = cls.build_adder(n-1, reg_1_2, reg_2_2, carry)
        
        
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
        Constructs a carry lookahead circuit for 4-bit addition.

        Args:
            reg1 (list[str]): The first binary register as a list of string labels.
            reg2 (list[str]): The second binary register as a list of string labels.
            c0 (str): The label for the initial carry input to the most significant bit.

        Returns:
            bool_circ: A boolean circuit representing the carry lookahead addition of `reg1` and `reg2`
                       with an initial carry, constructed as a composed logic graph.
        """

        # I do not understand the well-formedness of the circuit checks, as 
        assert len(reg1) == 4 and len(reg2) == 4

        def create_binary_gate(a, b, gate):
            n = g.add_node(label=gate)
            g.add_edge(a, n)
            g.add_edge(b, n)
            return n

        g = open_digraph.empty()

        # inputs
        r1 = [g.add_node(label='') for _ in reg1]
        r2 = [g.add_node(label='') for _ in reg2]

        for i in range(4):
            g.add_input_node(r1[i], label=reg1[i])
        for i in range(4):
            g.add_input_node(r2[i], label=reg2[i])

        # first carry
        c0_node = g.add_node(label='')
        g.add_input_node(c0_node, label=c0)
        carry = [c0_node]

        # generate and propagate
        generate, propagate = [], []
        for a, b in zip(r1, r2):
            generate.append(create_binary_gate(a, b, '&'))
            p = create_binary_gate(a, b, '^')
            #Adding a copy node to pass is_well_formedness check
            cp = g.add_node(label='')
            g.add_edge(p, cp)
            propagate.append(cp)

        # c by recursive relation
        for i in range(4):
            p_and_c = create_binary_gate(propagate[i], carry[i], '&')
            ci     = create_binary_gate(generate[i], p_and_c, '|')
            #adding a copy node to pass is_well_formedness check
            cp = g.add_node(label='')
            g.add_edge(ci, cp)
            carry.append(cp)

        # sum bits pi ^ ci
        sums = [create_binary_gate(propagate[i], carry[i], '^') for i in range(4)]

        # outputs
        for i in range(4):
            g.add_output_node(sums[i], label=f"s{i}")
        g.add_output_node(carry[-1], label="c4")
        return bool_circ(g)
    
    @classmethod
    def generate_4bit_encoder(cls: Type[TB], bit1: str, bit2: str, bit3: str, bit4: str) -> 'bool_circ':
        output_1 = f"(({bit1})^({bit2})^({bit4}))"
        output_2 = f"(({bit1})^({bit3})^({bit4}))"
        output_3 = f"({bit1})"
        output_4 = f"(({bit2})^({bit3})^({bit4}))"
        output_5 = f"({bit2})"
        output_6 = f"({bit3})"
        output_7 = f"({bit4})"

        return parse_parentheses(output_1, output_2, output_3, output_4, output_5, output_6, output_7)[0]

    @classmethod
    def generate_4bit_decoder(cls: Type[TB], bit1: str, bit2: str, bit3: str, bit4: str, bit5: str, bit6: str, bit7: str) -> 'bool_circ':
        # f_l = first_line
        xor_f_l_1 = f"(({bit1})^({bit3})^({bit5})^({bit7}))"
        xor_f_l_2 = f"(({bit2})^({bit3})^({bit6})^({bit7}))"
        xor_f_l_3 = f"(({bit4})^({bit5})^({bit6})^({bit7}))"

        output_1 = f"((({xor_f_l_1})&({xor_f_l_2})&(~{xor_f_l_3}))^({bit3}))"
        output_2 = f"((({xor_f_l_1})&(~{xor_f_l_2})&({xor_f_l_3}))^({bit5}))"
        output_3 = f"(((~{xor_f_l_1})&({xor_f_l_2})&({xor_f_l_3}))^({bit6}))"
        output_4 = f"((({xor_f_l_1})&({xor_f_l_2})&({xor_f_l_3}))^({bit7}))"

        return parse_parentheses(output_1, output_2, output_3, output_4)[0]

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

        # first 4‑bit block with initial carry
        circ = cls.carry_lookahead_4(reg1[0:4], reg2[0:4], carry)

        # for each subsequent 4‑bit block
        for i in range(1, blocks):
            c_label = f"c{4*i}"
            blk = cls.carry_lookahead_4(
                reg1[4*i:4*(i+1)],
                reg2[4*i:4*(i+1)],
                c_label
            )
            merged = circ.parallel(blk)


            #merge the carry out of the previous block with the carry in of the next block
            # find the carry out of the previous block
            out_id = next(
                oid for oid in merged.get_outputs_ids()
                if merged.get_id_node_map()[oid].get_label() == c_label
            )
            parent = list(merged.get_id_node_map()[out_id].parents.keys())[0]
            merged.remove_node_by_id(out_id)

            # find the carry in of the next block
            in_id = next(
                iid for iid in merged.get_inputs_ids()
                if merged.get_id_node_map()[iid].get_label() == c_label
            )
            child = list(merged.get_id_node_map()[in_id].children.keys())[0]
            merged.remove_node_by_id(in_id)

            merged.add_edge(parent, child)
            circ = merged

        circ.display("circ", verbose=False)
        return bool_circ(circ)
            

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

