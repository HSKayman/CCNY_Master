import numpy as np
from itertools import product
import random

def G(A, s):
    return np.dot(A.T, s) % 2

def generate_all_possible_s(n):
    return [np.array(s, dtype=np.int8) for s in product([0, 1], repeat=n)]

def test_G_for_all_s(A):
    n = A.shape[0]
    all_s = generate_all_possible_s(n)
    all_outputs = set()

    for s in all_s:
        output = tuple(G(A, s))
        all_outputs.add(output)

    m = A.shape[1]
    expected_number_of_outputs = 2 ** m
    actual_number_of_outputs = len(all_outputs)

    return actual_number_of_outputs == expected_number_of_outputs

def generate_random_matrix(n, m):
    return np.random.randint(2, size=(n, m))

def test_random_matrices(num_matrices, n, m):
    for _ in range(num_matrices):
        A = generate_random_matrix(n, m)
        secure = test_G_for_all_s(A)
        print("Matrix A:\n", A)
        print("Is G secure with this A?", "Yes" if secure else "No", "\n")

# Parameters
num_matrices = 5  # Number of random matrices to test
n = 4  # Number of rows in A (and size of input vector s)
m = 3  # Number of columns in A (and size of output vector)

test_random_matrices(num_matrices, n, m)
