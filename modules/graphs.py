
from modules.node import node
from modules.open_digraph import open_digraph


def graph_de_prof_td_10():
    n0 = node(0, '', {}, {2:1, 3:1})
    n1 = node(1, '', {}, {2:1, 3:1, 4:1})
    n2 = node(2, '', {0:1, 1:1}, {5:1})
    n3 = node(3, '', {0:1, 1:1}, {5:1, 6:1})
    n4 = node(4, '', {1:1}, {6:1})
    n5 = node(5, '', {2:1, 3:1}, {})
    n6 = node(6, '', {3:1, 4:1}, {})
    graph_de_prof = open_digraph([], [], [n0, n1, n2, n3, n4, n5, n6])
    return graph_de_prof
