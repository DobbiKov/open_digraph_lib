from modules.open_digraph import *

n0 = node(0, 'i', {}, {1:1})
n1 = node(1, 'o', {0:0}, {})
g = open_digraph([0], [1], [n0, n1])
print(g)
