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