from modules.open_digraph import *
import inspect


def print_file_contents(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
        f.close()

def print_matrix(mat: list[list[int]]):
    biggest_len = 0
    for line in mat:
        for j in line:
            s = str(j)
            len_s = len(s)
            if len_s > biggest_len:
                biggest_len = len_s

    for line in mat:
        for num in line:
            s = str(num)
            print(s, end='')
            for i in range(biggest_len - len(s)):
                print(" ", end="")

            print("   ", end="")
        print()

# particular graph
# test1
print("Test 1, press Enter to continue")
input()
mat_graph1 = random_oriented_int_matrix(10, 5)
print_matrix(mat_graph1)

# test2
print("Test 2, press Enter to continue")
input()
graph1 = open_digraph.from_matrix(mat_graph1)
print(graph1.is_well_formed())
print(graph1.get_nodes_ids())

# test3
print("Test 3, press Enter to continue")
input()
graph1.display()

# test4
print("Test 4, press Enter to continue")
input()
graph1.add_input_node(1)
print(graph1.is_well_formed())
print(graph1.get_nodes_ids())
# graph1.add_output_node(5)
# test5
print("Test 5, press Enter to continue")
input()
graph1.display("after_add_input")
