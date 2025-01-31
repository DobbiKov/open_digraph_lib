import sys
import os
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root

from modules.open_digraph import *

import graphviz

def vizualize_graph(graph):
  dot = graphviz.Digraph()

  with dot.subgraph(name='inputs') as s:
    s.attr(rank='same')
    for i in graph.inputs:
      nd = graph.nodes[i]
      s.node(str(nd.id), nd.label, shape='none')
  with dot.subgraph(name='outputs') as s:
    s.attr(rank='same')
    for i in graph.outputs:
      nd = graph.nodes[i]
      s.node(str(nd.id), nd.label)  
  for i in graph.nodes.keys():
    if (i not in graph.inputs )and (i not in graph.outputs):
      nd = graph.nodes[i]
      dot.node(str(nd.id), nd.label)  
  stack = graph.inputs

  def run(ind):
    if(ind == len(stack)):
      return
    if stack[ind] in graph.outputs:

      run(ind+1)
    else:
      for c in graph[stack[ind]].children:
        dot.edge(str(graph[stack[ind]].id), str(graph[c].id))
        if c not in stack:
          stack.append(c)
      run(ind+1)
  run(0)

  
  
  return dot

n0 = node(0, 'x0', {}, {4:4})
n1 = node(1, 'x1', {}, {5:5} )
n2 = node(2, 'x2', {}, {3:3})
n3 = node(3, 'copy', {2:2}, {4:4, 7:7})
n4 = node(4, '|', {0:0, 3:3}, {6:6})
n5 = node(5, 'copy', {1:1}, {6:6, 7:7})
n6 = node(6, '|', {4:4, 5:5}, {9:9})
n7 = node(7, '&', {5:5, 3:3},{8:8})
n8 = node(8, '~', {7:7}, {9:9})
n9 = node(9, '&', {6:6, 8:8}, {})

graph = open_digraph(
    [0,1,2], [9], [n0, n1,n2,n3,n4,n5,n6,n7,n8,n9]
)

dot = vizualize_graph(graph)

dot.render('graph', view=True)
