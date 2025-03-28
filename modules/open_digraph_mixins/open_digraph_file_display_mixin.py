import os
from modules.node import node

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphFileDisplayMixin(object):
    @classmethod
    def from_dot_file(cls: Type[T], path : str, verbose = False):
        """
        Reads a dot file given path and returns graph read from the file

        Args:
            path(str) - path where to read file from
        Returns:
            open_digraph
        """
        graph = cls.empty()
        with open(path, 'r') as f:
            lines = f.readlines()
            lines = iter(lines)
            nodes = {}
            inputs = []
            outputs = []
            for line in lines:
                line = line.strip()
                if '->' in line:
                    src, tgt = line.split('->')
                    src = int(src.strip().strip('v'))
                    tgt = int(tgt.strip().strip(';').strip('v'))
                    if src not in nodes:
                        nodes[src] = node(src, str(src), {}, {})
                    if tgt not in nodes:
                        nodes[tgt] = node(tgt, str(tgt), {}, {})
                    nodes[src].add_child_id(tgt)
                    nodes[tgt].add_parent_id(src)
                elif 'subgraph inputs' in line:
                    while '}' not in line:
                        line = next(lines).strip()
                        if 'v' in line:
                            parts = line.split(' ')
                            node_id = int(parts[0].strip().lstrip('v'))
                            label = parts[1].split('=')[1].strip('"')
                            inputs.append(node_id)
                            if node_id not in nodes:
                                nodes[node_id] = node(node_id, label, {}, {})
                            else:
                                nodes[node_id].set_label(label)
                elif 'subgraph outputs' in line:
                    while '}' not in line:
                        line = next(lines).strip()
                        if 'v' in line:
                            parts = line.split(' ')
                            node_id = int(parts[0].strip().lstrip('v'))
                            label = parts[1].split('=')[1].strip('"')
                            outputs.append(node_id)
                            if node_id not in nodes:
                                nodes[node_id] = node(node_id, label, {}, {})
                            else:
                                nodes[node_id].set_label(label)

                elif '[label=' in line:
                    node_id, label = line.split('[label=')
                    node_id = int(node_id.strip().lstrip('v'))
                    parts = label.split('"')
                    if len(parts) >= 2:
                        label = parts[1].strip()
                    else:
                        label = label.strip().strip('[];')
                    if node_id not in nodes:
                        nodes[node_id] = node(node_id, label, {}, {})
                    else:
                        nodes[node_id].set_label(label)
            graph.nodes = nodes
            graph.set_inputs(inputs)
            graph.set_outputs(outputs)
            return graph
            


    def save_as_dot_file(self: T, path: str, verbose: bool = False) -> None:
        """
        Save the given graph to the file using given path (if given verbose is True, adds ids of each node to the labels)

        Args:
            path(str) - path to the file
            verbose(bool) - True if add ids to the labels and False otherwise
        """
        def write_node(f, node):
            w_id = ""
            if verbose:
                w_id = node.get_id()
            f.write(f"v{node.get_id()} [label=\"{node.get_label()}{w_id}\" ")
            if node.get_id() in self.get_inputs_ids():
                f.write(f"shape=diamond")
            elif node.get_id() in self.get_outputs_ids():
                f.write(f"shape=box")
            f.write(f"]\n")

        with open(path, "w") as f:
            f.write("digraph G{\n")

            f.write("subgraph inputs{\n")
            f.write("rank=same;\n")
            for node in self.get_nodes():
                if node.get_id() in self.get_inputs_ids():
                    write_node(f, node)
            f.write("}\n")

            f.write("subgraph outputs{\n")
            f.write("rank=same;\n")
            for node in self.get_nodes():
                if node.get_id() in self.get_outputs_ids():
                    write_node(f, node)
            f.write("}\n")

            for node in self.get_nodes():
                if node.get_id() in self.get_outputs_ids() or node.get_id() in self.get_inputs_ids():
                    continue
                write_node(f, node)

            for node in self.get_nodes():
                for child in node.get_children().keys():
                    for i in range(node.get_children()[child]):
                        f.write(f"v{node.get_id()} -> v{int(child)};\n")
            f.write("}\n")
            f.close()
    def display(self: T, file_name='display_graph', dir="display", verbose: bool = False):
        """
        Displays the graph in a pdf file
        Args:
            file_name(str) - file name that the file will have (default: display_graph)
            dir(str) - folder where the files to save to (default: display)
            verbose(bool) - default: False, if set to true, the node's id will be written near the label
        """
        os.system(f"mkdir -p {dir}")
        file_name_dot = f"{file_name}.dot"
        file_name_pdf = f"{file_name}.pdf"
        self.save_as_dot_file(f"./{dir}/{file_name_dot}", verbose)
        os.system(f"dot -Tpdf ./{dir}/{file_name_dot} -o ./{dir}/{file_name_pdf}")

        os.system(f"open ./{dir}/{file_name_pdf}")
        # os.system(f"okular ./{dir}/{file_name_pdf}")

        #if os.system(f"python3 -m webbrowser -t \"./{file_name_pdf}\"") != 0:

        #os.remove(f"./{file_name_dot}")
        #os.remove(f"./{file_name_pdf}")
