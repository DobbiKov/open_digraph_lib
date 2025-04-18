from modules.node import node

from typing import TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphComposeParallelSplitMixin(object):
    def iparallel(self: T, g) -> None:
        """
        Adds to the graph a given graph g
        
        Args:
            g: open_digraph - graph to add 
        """
        newg = g.copy()
        newg.shift_indices(self.max_id() + 1)
        # Adds g parallel to self
        for node in newg.get_nodes():
            self.nodes[node.get_id()] = node

        
        for input in newg.get_inputs_ids():
            self.add_input_id(input)
        for output in newg.get_outputs_ids():
            self.add_output_id(output)

    def parallel(self: T, g):
        """
        Returns a sum of the two graphs
        Args:
            g(open_digraph) - a graph to add with
        Returns:
            open_digraph
        """
        newf = self.copy()
        newf.iparallel(g)
        return newf
    
    def icompose(self: T, g):
        """
        Composes the graph with a given graph g

        Args:
            g(open_digraph) - a graph to compose with
        """
        assert(len(self.get_inputs_ids()) == len(g.get_outputs_ids()))
        newg = g.copy()
        newg.shift_indices(self.max_id() + 1)
        # Adds g sequential to self
        for node in newg.get_nodes():
            self.nodes[node.get_id()] = node
        for input, output in zip(self.get_inputs_ids(), newg.get_outputs_ids()):
            self.add_edge(output, input)
        self.set_inputs(newg.get_inputs_ids())
    
    def compose(self: T, g):
        """
        Returns a composition of the graph with a given graph g

        Args:
            g(open_digraph) - a graph to compose with
        Returns: 
            open_digraph
        """
        newf = self.copy()
        newf.icompose(g)
        return newf
    
    def connected_components(self: T) -> tuple[int, dict[int, list[node]]]:
        """
        Returns a list of connected components of the graph

        Returns:
            (int, dict[int, list[node]])
        """
        def dfs(node_id, visited, component):
            # depth first search
            visited.add(node_id)
            component.append(node_id)
            for child in self[node_id].get_children():
                if child not in visited:
                    dfs(child, visited, component)
            for parent in self[node_id].get_parents():
                if parent not in visited:
                    dfs(parent, visited, component)

        visited = set()
        components = []
        for node_id in self.get_nodes_ids():
            if node_id not in visited:
                component = []
                dfs(node_id, visited, component)
                components.append(component)

        return len(components), {i: component for i, component in enumerate(components)}

    def split(self: T):
        """
        Splits the graph into connected components
        """
        n, components = self.connected_components()
        res = []
        for i in range(n):
            comp = components[i]
            tmp = self.empty()

            old_to_new = {}
            new_to_old = {}
            for node_id in comp:
                tmpid = tmp.add_node(self[node_id].get_label())
                old_to_new[node_id] = tmpid
                new_to_old[tmpid] = node_id
                if(node_id in self.get_inputs_ids()):
                    tmp.add_input_id(tmpid)
                if(node_id in self.get_outputs_ids()):
                    tmp.add_output_id(tmpid)
            
            for node_id in comp:
                out = self[node_id].get_children()
                for key, value in out.items():
                    tmp.add_edges([[old_to_new[node_id], old_to_new[key]] for _ in range(value)])
            res.append(tmp)
                
        
        return res
