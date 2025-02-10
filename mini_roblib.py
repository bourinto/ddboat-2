import numpy as np


def scalarprod(u, v):  # scalar product
    u, v = u.flatten(), v.flatten()
    return sum(u[:] * v[:])


def rotuv(u, v):  # returns rotation with minimal angle  such that  v=R*u
    # see https://en.wikipedia.org/wiki/Rotation_matrix#Vector_to_vector_formulation
    u = np.array(u).reshape(3, 1)
    v = np.array(v).reshape(3, 1)
    u = (1 / np.linalg.norm(u)) * u
    v = (1 / np.linalg.norm(v)) * v
    c = scalarprod(u, v)
    A = v @ u.T - u @ v.T
    return np.eye(3, 3) + A + (1 / (1 + c)) * A @ A


def sawtooth(x):
    return (x + np.pi) % (2 * np.pi) - np.pi
