# API Reference - bool_circ Module

The `bool_circ` class extends the `open_digraph` class to model boolean circuits. It enforces additional constraints and provides methods for boolean circuit transformations, evaluations, and generation.

## bool_circ Class

### Constructor

`bool_circ(g: open_digraph, debug: bool = False)`

- **g (open_digraph):** The graph to convert into a boolean circuit.
- **debug (bool):** When set to True, the circuit is created regardless of validation; otherwise, a non‑well-formed circuit is replaced by an empty graph.

### Methods

#### Validation

- `is_well_formed()`
  Checks if the circuit satisfies the following constraints:
  - The circuit is acyclic.
  - Nodes satisfy degree constraints:
    - Input nodes have no parents and one child.
    - Gate nodes like `&`, `|`, `^` have outdegree 1.
    - `~` nodes have one parent and one child.
    - Constant nodes (‘1’, ‘0’) have no outgoing edges.

#### Transformations

- `constant_copy_transform(copy_id: int)`
  Transforms a constant node connected to a copy node by creating fresh constants for each child of the copy node.

- `constant_not_transform(not_id: int)`
  Simplifies a NOT gate connected to a constant node by replacing it with the inverted constant.

- `transform_and_zero(and_id: int)`
  Simplifies an AND gate with a `0` input by removing the gate and connecting `0` to its child.

- `transform_and_one(and_id: int)`
  Simplifies an AND gate with a `1` input by removing the `1` and rewiring the gate.

- `transform_or_zero(or_id: int)`
  Simplifies an OR gate with a `0` input by removing the `0` and rewiring the gate.

- `transform_or_one(or_id: int)`
  Simplifies an OR gate with a `1` input by removing the gate and connecting `1` to its child.

- `transform_xor_zero(xor_id: int)`
  Simplifies an XOR gate with a `0` input by removing the `0` and rewiring the gate.

- `transform_xor_one(xor_id: int)`
  Simplifies an XOR gate with a `1` input by adding a NOT gate between the XOR and its child.

- `transform_in_zero(node_id: int)`
  Removes a node with no inputs and replaces it with a `0` constant.

- `transform_in_one(node_id: int)`
  Removes a node with no inputs and replaces it with a `1` constant.

- `transform_associative_xor(node_id: int)`
  Simplifies nested XOR gates by associativity.

- `transform_involution_xor(node_id: int)`
  Simplifies XOR gates with duplicate inputs.

- `transform_erase_operator(node_id: int)`
  Removes redundant operators based on their context.

- `transform_xor_if_has_parent_not(node_id: int)`
  Simplifies XOR gates with NOT parents.

- `transform_copy_if_has_parent_not(node_id: int)`
  Simplifies copy nodes with NOT parents.

- `transform_not_involution(node_id: int)`
  Removes consecutive NOT gates.

#### Evaluation

- `evaluate()`
  Applies all transformation rules iteratively until no more transformations are possible.

#### Circuit Generation

- `from_number(number: int, size: int = 8) -> bool_circ`
  Creates a boolean circuit representing a binary number.

- `random_bool_circ_from_graph(graph: open_digraph, inputs: int = 1, outputs: int = 1) -> bool_circ`
  Generates a random boolean circuit from a given graph.

- `build_adder(n: int, reg1: list[str], reg2: list[str], carry: str) -> bool_circ`
  Constructs an n-bit binary adder circuit.

- `carry_lookahead_4(reg1: list[str], reg2: list[str], c0: str) -> bool_circ`
  Constructs a 4-bit carry-lookahead adder.

- `carry_lookahead_4n(reg1: list[str], reg2: list[str], carry: str) -> bool_circ`
  Constructs a 4n-bit carry-lookahead adder.

- `generate_4bit_encoder(bit1: str, bit2: str, bit3: str, bit4: str) -> bool_circ`
  Generates a 4-bit encoder circuit.

- `generate_4bit_decoder(bit1: str, bit2: str, bit3: str, bit4: str, bit5: str, bit6: str, bit7: str) -> bool_circ`
  Generates a 4-bit decoder circuit.
