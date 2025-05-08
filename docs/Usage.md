# Usage Examples

This section contains examples to create graphs, boolean circuits, and visualize them.

## Creating a Graph
```py
from modules.open_digraph import node, open_digraph

# Create nodes
n0 = node(0, 'input', {}, {1: 1})
n1 = node(1, 'middle', {0: 1}, {2: 1})
n2 = node(2, 'output', {1: 1}, {})

# Create a graph with designated input/output nodes
g = open_digraph(inputs=[0], outputs=[2], nodes=[n0, n1, n2])
g.assert_is_well_formed()
```

## Creating a Boolean Circuit
```py
from modules.open_digraph import node, open_digraph
from modules.bool_circ import bool_circ

n0 = node(0, '0', {}, {1: 1})
n1 = node(1, '&', {0: 1}, {2: 1})
n2 = node(2, '1', {1: 1}, {})

g = open_digraph(inputs=[0], outputs=[2], nodes=[n0, n1, n2])
circuit = bool_circ(g)
print(circuit.is_well_formed())
```

## Visualizing a Graph
```py
from modules.open_digraph import node, open_digraph
from modules.viz import vizualize_graph

n0 = node(0, 'A', {}, {1: 1})
n1 = node(1, 'B', {0: 1}, {})
g = open_digraph(inputs=[0], outputs=[1], nodes=[n0, n1])
g.display()
```

## Generating Random Graphs
```py
from modules.open_digraph import open_digraph

# Generate a random graph with 5 nodes, max edge weight of 6, 2 inputs, and 2 outputs
g = open_digraph.random(5, 6, 2, 2, loop_free=True)
print(g)
```

## Composing Graphs
```py
from modules.open_digraph import node, open_digraph

# Create two simple graphs
g1 = open_digraph(
    inputs=[0],
    outputs=[1],
    nodes=[
        node(0, 'A', {}, {1: 1}),
        node(1, 'B', {0: 1}, {})
    ]
)
g2 = open_digraph(
    inputs=[0],
    outputs=[1],
    nodes=[
        node(0, 'C', {}, {1: 1}),
        node(1, 'D', {0: 1}, {})
    ]
)

# Compose the two graphs
g_composed = g1.compose(g2)
print(g_composed)
```

## Splitting Graphs into Components
```py
from modules.open_digraph import open_digraph

# Create a graph with two disconnected components
g = open_digraph(
    inputs=[],
    outputs=[],
    nodes=[
        node(0, 'A', {}, {1: 1}),
        node(1, 'B', {0: 1}, {}),
        node(2, 'C', {}, {3: 1}),
        node(3, 'D', {2: 1}, {})
    ]
)

# Split the graph into connected components
components = g.split()
for i, comp in enumerate(components):
    print(f"Component {i}:")
    print(comp)
```

## Evaluating Boolean Circuits
```py
from modules.bool_circ import *

num_1_bc = bool_circ.from_number(2, 4)
num_2_bc = bool_circ.from_number(3, 4)

num_1 = [ num_1_bc.get_id_node_map()[idx].get_label() for idx in num_1_bc.get_inputs_ids]
num_2 = [ num_2_bc.get_id_node_map()[idx].get_label() for idx in num_2_bc.get_inputs_ids]

adder_1 = bool_circ.build_adder(2, num_1, num_2, '0')
adder_1.display('adder_1')

adder_1.evaluate()
adder_1.display('adder_1_evaluated')
print(get_result_of_evaluated_additioner(adder_1))
print(add_two_numbers(14, 27))
```

## Visualizing Boolean Circuits
```py
from modules.bool_circ import bool_circ

# Generate a 4-bit encoder circuit
encoder = bool_circ.generate_4bit_encoder('0', '1', '0', '1')
encoder.display("encoder")
```