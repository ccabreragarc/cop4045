# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Display a table and chart for a user-entered math function

import math
import matplotlib.pyplot as pyplot

# -----------------------------
# Initial variable declarations
# -----------------------------
fun_str = ""
xmin = 0.0
xmax = 0.0
domain = (xmin, xmax)
ns = 0


def plot_function(fun_str, domain, ns):
    xs = []
    ys = []
    xmin = domain[0]
    xmax = domain[1]
    sample_counter = 0
    dx = 0.0
    x = xmin
    y = 0.0

    if ns == 1:
        dx = 0.0
    else:
        dx = (xmax - xmin) / (ns - 1)

    # Evaluate the typed expression for each x value.
    while sample_counter < ns:
        xs.append(x)
        y = eval(fun_str)
        ys.append(y)
        x = x + dx
        sample_counter = sample_counter + 1

    print("{:>10} {:>10}".format("x", "y"))
    print("--------------------")

    sample_counter = 0
    while sample_counter < ns:
        print("{:+10.4f} {:+10.4f}".format(xs[sample_counter], ys[sample_counter]))
        sample_counter = sample_counter + 1

    pyplot.plot(xs, ys, "ro-")
    pyplot.xlabel("x")
    pyplot.ylabel("y")
    pyplot.title(fun_str)
    pyplot.grid(True)
    pyplot.show()
    pyplot.clf()


fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))
domain = (xmin, xmax)

plot_function(fun_str, domain, ns)
