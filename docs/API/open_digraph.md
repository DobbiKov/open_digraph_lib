# API Reference - open_digraph Module

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
- `copy()` - Returns a deep copy of the node.

## open_digraph Class

### Constructor

`open_digraph(inputs: list[int], outputs: list[int], nodes: list[node])`

- **inputs:** List of node IDs acting as inputs.
- **outputs:** List of node IDs acting as outputs.
- **nodes:** A list of `node` objects.

### Main Methods

#### Getters
- `get_inputs_ids()` - Returns the IDs of input nodes.
- `get_outputs_ids()` - Returns the IDs of output nodes.
- `get_id_node_map()` - Returns a mapping of node IDs to node objects.
- `get_nodes()` - Returns all nodes in the graph.
- `get_nodes_ids()` - Returns the IDs of all nodes.

#### Modifiers
- `add_edge(src, tgt)` - Adds a directed edge between nodes.
- `add_node(label, parents, children)` - Creates a new node.
- `add_input_node(point_to_id)` - Creates an input node pointing to a target.
- `add_output_node(point_from_id)` - Creates an output node pointed from a source.
- `remove_edge(src, tgt)` - Removes one edge.
- `remove_parallel_edges(src, tgt)` - Removes all edges between two nodes.
- `remove_node_by_id(id)` - Removes a node, updating connections.

#### Composition and Parallelism
- `icompose(g)` - Composes the graph with another graph in-place.
- `compose(g)` - Returns a new graph composed with another graph.
- `iparallel(g)` - Adds another graph in parallel in-place.
- `parallel(g)` - Returns a new graph with another graph added in parallel.

#### Well-Formedness
- `is_well_formed()` - Checks if the graph is well-formed.
- `assert_is_well_formed()` - Asserts that the graph is well-formed.

#### Matrix Operations
- `adjacancy_matrix()` - Returns the graph’s adjacency matrix.
- `from_matrix(mat)` - Constructs a graph from an adjacency matrix.

#### Display and File Operations
- `save_as_dot_file(path, verbose=False)` - Saves the graph as a DOT file.
- `save_as_pdf_file(file_name, dir, verbose=False)` - Saves the graph as a PDF.
- `display(file_name, dir, verbose=False)` - Displays the graph using Graphviz.
- `from_dot_file(path)` - Reads a DOT file and creates a graph.

#### Random Graph Generation
- `random(n, bound, inputs, outputs, form, loop_free)` - Generates a random graph.

#### Other Helpers
- `new_id()` - Returns an available ID.
- `shift_indices(n)` - Shifts all node IDs.
- `fuse_nodes(id1, id2, label)` - Fuses two nodes into one.
- `empty()` - Returns an empty graph.
- `copy()` - Returns a deep copy of the graph.
