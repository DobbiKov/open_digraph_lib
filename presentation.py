from modules.open_digraph import *
import inspect


def print_file_contents(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
        f.close()

# particular graph
n0 = node(0, '0i', {3:1}, {1:1, 2:2})
n1 = node(1, '1i', {0:1}, {3:3})
n2 = node(2, '2o', {0:2}, {})
n3 = node(3, '3a', {1:3, 4:1}, {0:1})
n4 = node(4, '4i', {}, {3:1})
graph = open_digraph([4], [2], 
                  [n0, n1, n2, n3, n4])

print("Un graphe particulier")
graph.save_as_dot_file("./dot.dot")
print("Le contenu du fichier souvegarder de ce graph:")
print_file_contents("./dot.dot")
graph.display()

graphNew = open_digraph.from_dot_file("./dot.dot")
graphNew.display('new_graph')

# random graph
print()
print("Un graphe aléatoire")
rand_graph = open_digraph.random(5, 6, 2, 2, loop_free=False)
rand_graph.display("random_graph")


