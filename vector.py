import math

def norm(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def squared_norm(vec):
    return vec[0]*vec[0] + vec[1]*vec[1]

def divide(vec, scalar):
    return (vec[0] / scalar, vec[1] / scalar)

def multiply(vec, scalar):
    return (vec[0] * scalar, vec[1] * scalar)

def add(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])

def substract(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])

def normalize(vec):
    return divide(vec, norm(vec))