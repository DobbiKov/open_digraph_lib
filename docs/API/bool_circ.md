# API Reference – bool_circ Module

The `bool_circ` class extends the open directed graph to model boolean circuits. It enforces additional constraints:

## bool_circ Class

### Constructor

`bool_circ(g: open_digraph, debug: bool = False)`

- **g (open_digraph):** The graph to convert into a boolean circuit.
- **debug (bool):** When set to True, the circuit is created regardless of validation; otherwise, a non‑well-formed circuit is replaced by an empty graph.

### Methods

- `is_well_formed()`  
  Checks:
  - The circuit is acyclic.
  - Nodes satisfy degree constraints:  
    - Input nodes have no parents and one child.  
    - Gate nodes like `&`, `|`, `^` have outdegree 1;  
    - `~` nodes have one parent and one child;  
    - Constant nodes (‘1’, ‘0’) have no outgoing edges.
  
The class inherits all methods from `open_digraph`.
