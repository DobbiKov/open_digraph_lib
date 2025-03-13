DobbiKov: You're an astonishing python engineer that works in Microsoft. You're given a task to write a complete documentation so it can be reused even by programmers who have learnt python just yesterday. Read and analyse all the project and write the documentation for whole the project. 

GitHub Copilot: Below is a complete documentation for the project. You can save this as a Markdown file (for example, DOCUMENTATION.md) in your project root.

---

# Open Digraph Library Documentation

Welcome to the Open Digraph Library! This documentation explains the purpose, structure, installation, usage, and API details of the project. Even if you are new to Python, you will be guided step by step.

---

## Table of Contents

1. Overview
2. Project Structure
3. Installation
4. Running the Project
    - Running the Worksheet
    - Running the Tests
5. Modules Overview
    - modules/open_digraph.py
    - modules/bool_circ.py
    - modules/viz.py
6. API Details
    - node Class
    - open_digraph Class
    - Helper Methods in open_digraph
    - Boolean Circuit (bool_circ)
    - Visualization (viz)
7. Examples and Usage
8. Contributing and Further Information

---

## Overview

The Open Digraph Library is a Python project for creating and manipulating directed graphs (digraphs) with open inputs and outputs. It further includes functionality for building boolean circuits (extending the graph model) and visualizing the graphs using Graphviz.

Key features include:
- **Node-based graph representation:** Each node has a unique identifier, a label, parent nodes (with multiplicity), and child nodes.
- **Open directed graph:** A graph with designated input and output nodes.
- **Support for random graph generation:** Create adjacency matrices with various properties and convert these matrices into graphs.
- **Boolean Circuit Validation:** Verify if a graph qualifies as a valid boolean circuit based on specific constraints.
- **Graph Visualization:** Visualize graphs using the Graphviz package.
- **Extensive test suite:** Unit tests ensure that all functions work correctly.

---

## Project Structure

The main folders and files are described below:

    /projet_info
    ├── .gitignore                              # Files and folders to ignore in Git
    ├── README.md                               # Basic project overview
    ├── requirements.txt                        # External packages (graphviz)
    ├── run.sh                                  # Script to run the worksheet and view the output PDF
    ├── tests.sh                                # Shell script to run unit tests
    ├── worksheet.py                            # Sample script demonstrating library usage
    ├── graph                                   # Sample dot file for a graph
    └── modules
        ├── open_digraph.py                     # Contains the node and open_digraph classes and related functions
        ├── bool_circ.py                        # Implements a boolean circuit class (inherits from open_digraph)
        └── viz.py                              # Graph visualization functions using Graphviz

The tests (located in the tests folder) demonstrate how the classes and functions are used. They use Python's `unittest` framework.

---

## Installation

1. **Python Installation:**  
   Make sure you have Python 3 installed on your system.

2. **Install Graphviz:**  
   This project uses Graphviz for visualization.

   On macOS, install via Homebrew:
   ```sh
   brew install graphviz
   ```

3. **Install Python Dependencies:**  
   Use pip to install required packages.
   ```sh
   pip3 install -r requirements.txt
   ```

---

## Running the Project

### Running the Worksheet

The worksheet.py file contains sample usage of the library. To run it:

```sh
./run.sh
```

This script runs the worksheet, saves the graph as a DOT file, converts it to PDF, and opens the PDF on macOS.

### Running the Tests

The tests are located in the tests folder. To run all tests, use:
```sh
./tests.sh
```
or run:
```sh
python3 -m unittest tests/*.py
```

---

## Modules Overview

### open_digraph.py

This module is the core of the library and defines two main classes:

- **node Class:**  
  Represents a node in the graph.
  - **Attributes:**  
    - `id`: unique integer identifier.
    - `label`: a string label.
    - `parents`: a dictionary mapping parent node IDs to their multiplicity.
    - `children`: a dictionary mapping child node IDs to their multiplicity.
  - **Methods:**  
    - Getters and setters for all attributes.
    - Methods to add or remove parent/child IDs.
    - Methods to compute indegree, outdegree, and total degree.
    - A `copy()` method for deep-copying nodes.

- **open_digraph Class:**  
  Represents an open directed graph with designated input and output nodes.
  - **Attributes:**
    - `inputs`: list of node IDs acting as inputs.
    - `outputs`: list of node IDs acting as outputs.
    - `nodes`: dictionary mapping node IDs to their corresponding node objects.
  - **Methods:**  
    - Getters for inputs, outputs, all nodes, and their IDs.
    - `add_edge(src, tgt)` to add a directed edge.
    - `add_node(label, parents, children)` to add a new node (automatically assigns a new unique ID).
    - `add_input_node(point_to_id)` and `add_output_node(point_from_id)` for creating new input/output nodes with correct constraints.
    - Methods to remove edges and nodes.
    - Various helper functions (e.g. `shift_indices()`, `new_id()`, `get_node_id_to_enumerate_mapping()`, etc.).
    - Functions to generate an adjacency matrix and to create a graph from an adjacency matrix.
    - Methods to check for graph acyclicity and well-formedness (`assert_is_well_formed()`).

### bool_circ.py

This module defines the **bool_circ** class that inherits from `open_digraph` and is used for creating boolean circuits. It adds:
- **Validation for Boolean Circuits:**  
  The `is_well_formed()` method checks if the circuit is valid (acyclic, and with specific constraints on the nodes’ degrees based on their labels, such as:
  - Input nodes should have no parents and exactly one child.
  - Output nodes should have exactly one parent and no children.
  - Gate nodes (like AND, OR, XOR, NOT) have specified indegree and outdegree constraints.
- **Debug Option:**  
  The constructor accepts a `debug` flag that controls whether a non–well-formed circuit is rejected or allowed (emptying the graph).

### viz.py

The viz module provides functions to visualize the graph using Graphviz.
- **vizualize_graph(graph):**  
  Takes an `open_digraph` object and returns a Graphviz `Digraph` object.
  - It creates subgraphs for inputs and outputs and arranges nodes accordingly.
  - It then connects nodes by adding edges in the Graphviz DOT definition.
  
You can render and view your graph using the Graphviz API or by saving a DOT file and converting it to PDF.

---

## API Details

### node Class

**Constructor:**  
`node(identity, label, parents, children)`  
- `identity`: Unique integer identifier.
- `label`: A string representing the node label.
- `parents`: Dictionary mapping parent IDs to their multiplicity.
- `children`: Dictionary mapping child IDs to their multiplicity.

**Key Methods:**
- `get_id()`, `get_label()`, `get_parents()`, `get_children()`
- `set_id(value)`, `set_label(value)`, `set_parents(value)`, `set_children(value)`
- `add_child_id(child_id)`, `add_parent_id(parent_id)`
- `remove_child_once(child_id)`, `remove_parent_once(parent_id)`
- `remove_child_id(child_id)`, `remove_parent_id(parent_id)`
- `indegree()`, `outdegree()`, `degree()`
- `copy()`: Returns a deep copy of the node.

### open_digraph Class

**Constructor:**  
`open_digraph(inputs: list[int], outputs: list[int], nodes: list[node])`  

**Key Methods:**

- **Graph Structure Methods:**
  - `get_inputs_ids()`, `get_outputs_ids()`, `get_nodes_ids()`, `get_id_node_map()`, `get_nodes()`
  - `min_id()`, `max_id()`

- **Edge and Node Modification:**
  - `new_id()`: Finds and returns an available node ID.
  - `add_edge(src, tgt)`: Adds an edge from source node to target node.
  - `add_node(label, parents, children)`: Adds a new node with optional connections.
  - `add_input_node(point_to_id)`: Creates and returns a new input node that points to an existing node.
  - `add_output_node(point_from_id)`: Creates and returns a new output node that is pointed from an existing node.

- **Graph Modification and Validation:**
  - `remove_edge(src, tgt)`, `remove_parallel_edges(src, tgt)`
  - `remove_node_by_id(id)`, `remove_nodes_by_id(ids)`
  - `shift_indices(n)`: Shifts all node IDs by a constant offset.
  - `assert_is_well_formed()`: Raises an assertion error if the graph does not meet the well-formed criteria.
  - `is_well_formed()`: Returns a Boolean indicating whether the graph is well formed.
  - `is_acyclic()` and `is_cyclic()`: Check the cyclicity of the graph.

- **Adjacency and Random Graphs:**
  - `adjacancy_matrix()`: Returns the adjacency matrix representation for the graph.
  - `graph_from_adjacency_matrix(mat)`: Class method to build a graph from an adjacency matrix.
  - `random(...)`: Class method to generate random graphs based on given parameters.

### Boolean Circuit (bool_circ)

Inherits from the `open_digraph` class and adds additional constraints:
- **Constructor:**  
  `bool_circ(g: open_digraph, debug: bool=False)`
- **is_well_formed():**  
  Checks additional conditions based on the boolean circuit (e.g., input nodes must only have one outgoing connection, and gate types must satisfy specific in/out degree rules).
- If a provided graph does not meet these criteria and if `debug` is False, the circuit is replaced by an empty graph.

### Visualization (viz)

- **vizualize_graph(graph):**
  - Accepts an open directed graph and returns a Graphviz `Digraph` object.
  - Organizes nodes into subgraphs for inputs and outputs.
  - Traverses the graph to add edges accordingly.
  - You can render the returned DOT graph or save it to a file using the provided methods in `open_digraph` (e.g., `save_as_dot_file()`).

---

## Examples and Usage

### Creating and Handling a Graph

```py
from modules.open_digraph import node, open_digraph

# Create nodes
n0 = node(0, 'input', {}, {1: 1})
n1 = node(1, 'middle', {0: 1}, {2: 1})
n2 = node(2, 'output', {1: 1}, {})

# Create a graph with designated inputs and outputs
g = open_digraph(inputs=[0], outputs=[2], nodes=[n0, n1, n2])

# Add an edge and a new node
g.add_edge(1, 2)
new_node_id = g.add_node('extra', parents={1: 1}, children=None)

# Validate the graph
g.assert_is_well_formed()
```

### Creating a Boolean Circuit

```py
from modules.open_digraph import node, open_digraph
from modules.bool_circ import bool_circ

# Construct nodes (labels must conform to circuit constraints, e.g., '0', '1', '&', '|', '^', '~', etc.)
n0 = node(0, '0', {}, {1: 1})
n1 = node(1, '&', {0: 1}, {2: 1})
n2 = node(2, '1', {1: 1}, {})

# Create a graph and then a boolean circuit
g = open_digraph(inputs=[0], outputs=[2], nodes=[n0, n1, n2])
circuit = bool_circ(g)

# Check if the circuit is valid
print(circuit.is_well_formed())  # Should output True if all constraints are met
```

### Visualizing a Graph

```py
from modules.open_digraph import node, open_digraph
from modules.viz import vizualize_graph

# Create a sample graph
n0 = node(0, 'A', {}, {1: 1})
n1 = node(1, 'B', {0: 1}, {})
g = open_digraph(inputs=[0], outputs=[1], nodes=[n0, n1])

# Visualize the graph
dot = vizualize_graph(g)
dot.render('my_graph', view=True)
```

---

## Contributing and Further Information

- **Authors:**  
  - Yehor Korotenko  
  - Sipan Bareyan  
  - Ivan Kharkov

- **Repository:**  
  See the README.md for the GitHub repository link.

- **Extending the Library:**  
  Feel free to experiment with the code:
  - Add more node types and validation rules for boolean circuits.
  - Enhance visualization features (e.g., custom shapes, labels).
  - Improve testing by adding edge cases.

If you have any questions or suggestions, please contact the authors via their provided emails in the README.

---

This documentation should get you started on using and extending the Open Digraph Library. Happy coding!

