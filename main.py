from xmlrpc.client import boolean

import numpy as np
import re


def parse_file(f, mode):
    lines = f.readlines()
    # reading n, m and k from file, parsing with regex
    params = list(map(int, re.findall(r"\d+", lines[0])))
    n = params[0]  # n is not needed for this implementation
    m = params[1]  # m is the number of tasks
    k = params[2]  # k is the number of tasks to be ordered
    del params
    if mode == "ALL":
        adjacency_matrix = np.identity(m)
        for line in lines[1:-1]:
            if "<" in line:
                # processing the string to create a list, A < B < C -> ["A", "B", "C"]
                tasks = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line)
                for i in range(1, len(tasks)):
                    # < is transitiv, if A < B < C, not only A < B and B < C but also A < C are true
                    for j in range(i):
                        adjacency_matrix[ord(tasks[j][0]) - ord("A"), ord(tasks[i][0]) - ord("A")] += 1.0
        return adjacency_matrix
    elif mode == "SELECTED":
        adjacency_matrix = np.identity(k)
        selected = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', lines[-1])
        for line in lines[1:-1]:
            if "<" in line:
                tasks = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line)
                tasks[:] = [element for element in re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line) if
                            element in selected]
                for i in range(1, len(tasks)):
                    for j in range(i):
                        adjacency_matrix[selected.index(tasks[j][0]), selected.index(tasks[i][0])] += 1.0
        return adjacency_matrix


def transition_matrix(adjacency_matrix):
    row_sums = adjacency_matrix.sum(axis=1, keepdims=True)
    return adjacency_matrix / row_sums


def random_surfer(t_matrix, steps):
    matrix = (1 / (steps + 1)) * np.identity(len(t_matrix))
    for i in range(1, steps + 1):
        matrix += (1 / (steps + 1)) * np.linalg.matrix_power(t_matrix, i)
    return matrix


def evaluate(difficulties, mode, fn):
    if mode == "ALL":
        for j in range(len(difficulties)):
            acc = -1.0
            index = 0
            equal = False
            for i in range(len(difficulties)):
                if acc < difficulties[i]:
                    acc = difficulties[i]
                    equal = False
                    index = i
                elif acc == difficulties[i]:
                    equal = True
            print(f"{chr(index + ord('A'))} ", end="")
            if j < len(difficulties) - 1:
                if equal:
                    print("= ", end="")
                else:
                    print(">= ", end="")
            difficulties[index] = -1.0
    elif mode == "SELECTED":
        f = open(fn)
        ls = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', f.readlines()[-1])
        for j in range(len(difficulties)):
            acc = -1.0
            index = 0
            equal = False
            for i in range(len(difficulties)):
                if acc < difficulties[i]:
                    acc = difficulties[i]
                    equal = False
                    index = i
                elif acc == difficulties[i]:
                    equal = True
            print(f"{ls[index]} ", end="")
            if j < len(difficulties) - 1:
                if equal:
                    print("= ", end="")
                else:
                    print(">= ", end="")
            difficulties[index] = -1.0


# MODE = "ALL" : Ignore relevant tasks from file and order all tasks
# MODE = "SELECTED" : Only order tasks specified in file
MODE = "SELECTED"
np.set_printoptions(precision=3, suppress=True)

# IO
file_name = input("Please provide the path of the .txt-file containing the input: ")
if file_name == "0" or file_name == "1" or file_name == "2" or file_name == "3" or file_name == "4" or file_name == "5":
    # to test the examples given on https://bwinf.de/bundeswettbewerb/43/, you can just enter the number of the example
    file_name = f"schwierigkeiten{file_name}.txt"
file = open(file_name)

# calculate adjacency-matrix
ad_matr = parse_file(file, mode=MODE)
print(f"\nMatrix A:\n{ad_matr}\n")

# calculate transission-matrix
tr_matr = transition_matrix(ad_matr)
print(f"\nMatrix P:\n{tr_matr}\n")

# calculate random-surfer-matrix
matr = random_surfer(tr_matr, 500)
print(f"\nMatrix Q:\n{matr}\n")

# extract result form random-surfer-matrix and print order
result = matr.sum(0)
print(f"{result} (higher means harder)")
print("\nevaluation:")
evaluate(result.tolist(), mode=MODE, fn=file_name)