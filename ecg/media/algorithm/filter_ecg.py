import scipy as sp

# Basic functions
x = sp.random.random()
print("Random num: ", x)

x_sqrt = sp.sqrt(x)
print("Square root: ", x_sqrt)

matrix = sp.random.random(3)
print("Matrix: ", matrix)

matrix = sp.append(matrix, sp.random.random(2))
print("New matrix: ", matrix)


def add(x, y):
    return x+y


print("1+2 = ", add(1, 2))

# Complex functions
from scipy import linalg


def norm(start, end, num_elements):
    sx = sp.linspace(start, end, num_elements)
    return linalg.norm(sx)


def find_max_norm(start_range, end_range, num_elements):
    maximum = 0
    for i in start_range:
        for j in end_range:
            x = norm(i, j, num_elements)
            if x > maximum:
                maximum = x
    return maximum


print(find_max_norm(sp.linspace(0, 1, 10), sp.linspace(0, 5, 10), 100))


print(norm(2, 3, 100))

# Integrals
import scipy.integrate as integrate
from scipy import signal
from scipy.integrate import dblquad

result = integrate.quad(lambda x: x, 0, 4.5)
print("Integration of x on interval [0, 4.5]: ", result[0])


def gauss(x, sigma):
    return sp.exp(-x**2/(2*sigma**2))/sigma*sp.sqrt(2*sp.pi)


result = integrate.quad(lambda x: gauss(x, 1), -sp.inf, sp.inf)
print("Integration of Gaussian function on infinite intervals: ", result[0])
