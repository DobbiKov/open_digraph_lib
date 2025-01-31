import sys
import os
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root

from modules.open_digraph import *

import graphviz

def vizualize_graph(graph: open_digraph):
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

