import random
from modules.node import node

from typing import TYPE_CHECKING, Type, TypeVar, cast

if TYPE_CHECKING:
    from modules.open_digraph import open_digraph

T = TypeVar("T", bound="open_digraph")

class OpenDigraphMatrixMixin(object):
    def adjacancy_matrix(self: T) -> list[list[int]]:
        '''
        **Creates an adjacancy matrix corresponding to the graph**
        '''
        #TODO
        map = self.get_node_id_to_enumerate_mapping(True, True)
        n = len(map)
        res = [[0 for _ in range(n)] for _ in range(n)]
        for node_id, mat_id in map.items():
            for c_id, c_mult in self.get_id_node_map()[node_id].get_children().items():
                if c_id in self.get_inputs_ids() or c_id in self.get_outputs_ids(): # we do not count the edges with inputs and outputs
                    continue
                res[mat_id][map[c_id]]+=c_mult
        return res

    @classmethod
    def random(cls: Type[T], n: int, bound: int, inputs: int=0, outputs: int=0, form: str="free", loop_free: bool=True, random_function  = ( lambda: random.uniform(0.9,1) )) -> 'open_digraph':
        """
        Construct a random graph given constraints and type

        Args:
            n(int) - number of nodes
            bound(int) - limit of max possible edges pointing from one node to another
            inputs(int) - number of input nodes
            outputs(int) - number of output nodes
            form(str) - the form of the graph (free, DAG, oriented, undirected)
            loop_free(bool) - True if there must be no loops (from a node to the same node) and False otherwise
        Returns: 
            open_digraph
        """
        mat = []

        match form:
            case "free":
                mat = random_int_matrix(n, bound, loop_free, random_function)
            case "DAG":
                mat = random_triangular_int_matrix(n, bound, loop_free)
            case "oriented":
                mat = random_oriented_int_matrix(n, bound, loop_free)
            case "undirected":
                mat = random_symetric_int_matrix(n, bound, loop_free)

        # inputs outputs
        g = cls.from_matrix(mat)

        for i in range(inputs):
            g.add_input_node(random.randrange(n))
        for i in range(outputs):
            g.add_output_node(random.randrange(n))

        return g

    @classmethod
    def from_matrix(cls: Type[T], mat: list[list[int]]):
        """
        Construct open_digraph from the given adjacancy matrix

        Args:
            mat( list(list(int)) ) - a 2D matrix to construct graph from
        Returns:
            open_digraph
        """
        g = cls([], [], [])
        for i in range(len(mat)):
            g.add_node(str(i))
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                for k in range(mat[i][j]):
                    g.add_edge(i, j)
        return g


def random_int(bound, start=0, number_generator= (lambda: random.uniform(0,1))) -> int:
    return int(round(start + (bound-start)*number_generator()))

def random_int_list(n, bound, number_generator = (lambda: random.betavariate(1, 5))) -> list[int]:
    return [random_int(bound, number_generator=number_generator) for _ in range(n)]

def random_int_matrix(n, bound, null_diag=True, number_generator = (lambda: random.betavariate(1, 5))) -> list[list[int]]:
    res = [random_int_list(n, bound, number_generator=number_generator) for _ in range(n)]

    if null_diag == True:
        for i in range(n):
            res[i][i] = 0

    return res

def random_symetric_int_matrix(n, bound, null_diag=True,  number_generator = (lambda: random.betavariate(1, 5))) -> list[list[int]]:
    res = random_int_matrix(n, bound, null_diag, number_generator=number_generator)
    for i in range(n):
        for j in range(n):
            res[j][i] = res[i][j]
    return res

def random_oriented_int_matrix(n, bound, null_diag=True, number_generator = (lambda: random.betavariate(1, 5))) -> list[list[int]]:
    res = random_int_matrix(n, bound, null_diag, number_generator=number_generator)
    for i in range(n):
        for j in range(n):
            if res[i][j] != 0:
                res[j][i] = 0
    return res

def random_triangular_int_matrix(n, bound, null_diag=True, number_generator = (lambda: random.betavariate(1, 5))) -> list[list[int]]:
    res = random_int_matrix(n, bound, null_diag, number_generator=number_generator)
    c = int(not null_diag) #For null_diag see random_symmetric_int_matrix
    for i in range(n):
        for j in range(i+ c):
            # if i > j: 
            res[i][j] = 0
    return res

