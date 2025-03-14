# API Reference – open_digraph Module

This module is the core of the library. It defines:
- The `node` class that represents a node.
- The `open_digraph` class that represents an open directed graph.

## node Class

### Constructor

`node(identity, label, parents, children)`

- **identity (int):** Unique ID for the node.
- **label (str):** A string label.
- **parents (dict):** Mapping from parent node IDs to their multiplicities.
- **children (dict):** Mapping from child node IDs to their multiplicities.

### Key Methods

- `get_id()`, `get_label()`, `get_parents()`, `get_children()`
- `set_id(value)`, `set_label(value)`, `set_parents(value)`, `set_children(value)`
- `add_child_id(id)`, `add_parent_id(id)`
- `remove_child_once(id)`, `remove_parent_once(id)`
- `remove_child_id(id)`, `remove_parent_id(id)`
- `indegree()`, `outdegree()`, `degree()`
- `copy()` – Returns a deep copy of the node.

## open_digraph Class

### Constructor

`open_digraph(inputs: list[int], outputs: list[int], nodes: list[node])`

- **inputs:** List of node IDs acting as inputs.
- **outputs:** List of node IDs acting as outputs.
- **nodes:** A list of `node` objects.

### Main Methods

- **Getters:**  
  `get_inputs_ids()`, `get_outputs_ids()`, `get_id_node_map()`, `get_nodes()`, `get_nodes_ids()`
  
- **Modification:**  
  - `add_edge(src, tgt)` – Adds a directed edge between nodes.
  - `add_node(label, parents, children)` – Creates a new node.
  - `add_input_node(point_to_id)` – Creates an input node pointing to a target.
  - `add_output_node(point_from_id)` – Creates an output node pointed from a source.
  
- **Removers:**  
  - `remove_edge(src, tgt)` – Remove one edge.
  - `remove_parallel_edges(src, tgt)` – Remove all edges between two nodes.
  - `remove_node_by_id(id)` – Remove a node including updating connections.

- **Other Helpers:**
  - `new_id()` – Returns an available ID.
  - `shift_indices(n)` – Shifts all node IDs.
  - `assert_is_well_formed()` – Checks graph consistency.
  - `is_well_formed()`, `is_acyclic()`, `is_cyclic()`
  - `adjacancy_matrix()` – Returns the graph’s adjacency matrix.
  - `from_dot_file(path)` – Reads a DOT file and creates a graph.
  - `save_as_dot_file(path, verbose=False)` – Saves graph as DOT file.
  - `display()` – Renders and displays the graph using Graphviz. Takes optional `file_name` and `dir` arguments where `file_name` is the name of the output files and `dir` is a name of the folder where the files will be saved. 

- **Random Graph Generation:**  
  - `random(n, bound, inputs, outputs, form, loop_free)` – Generates a random graph.
