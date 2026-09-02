# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Solve and graph quadratic equations entered from the terminal

import math
import matplotlib.pyplot as pyplot

# -----------------------------
# Initial variable declarations
# -----------------------------
number_of_points = 150
domain_padding = 2.0
default_domain_radius = 5.0
a_text = ""
a_value = 0.0
b_value = 0.0
c_value = 0.0
discriminant = 0.0
x_one = 0.0
x_two = 0.0
x_opt = 0.0
x_min = 0.0
x_max = 0.0
dx = 0.0
x_value = 0.0
y_value = 0.0
point_counter = 0
xs = []
ys = []

while True:
    a_text = input("Enter a: ")

    if a_text == "":
        break

    a_value = float(a_text)
    b_value = float(input("Enter b: "))
    c_value = float(input("Enter c: "))

    discriminant = b_value**2 - 4 * a_value * c_value
    x_opt = -b_value / (2 * a_value)

    # Pick the graph domain so the roots or vertex are visible.
    if discriminant < 0:
        print("no real solutions")
        x_min = x_opt - default_domain_radius
        x_max = x_opt + default_domain_radius
    elif discriminant == 0:
        x_one = -b_value / (2 * a_value)
        print("one solution:", x_one)
        x_min = x_one - default_domain_radius
        x_max = x_one + default_domain_radius
    else:
        x_one = (-b_value - math.sqrt(discriminant)) / (2 * a_value)
        x_two = (-b_value + math.sqrt(discriminant)) / (2 * a_value)
        print("two solutions: x1=", x_one, "x2=", x_two)

        if x_one < x_two:
            x_min = x_one - domain_padding
            x_max = x_two + domain_padding
        else:
            x_min = x_two - domain_padding
            x_max = x_one + domain_padding

    xs = []
    ys = []
    dx = (x_max - x_min) / (number_of_points - 1)
    x_value = x_min
    point_counter = 0

    while point_counter < number_of_points:
        y_value = a_value * x_value**2 + b_value * x_value + c_value
        xs.append(x_value)
        ys.append(y_value)
        x_value = x_value + dx
        point_counter = point_counter + 1

    pyplot.plot(xs, ys, "ro-")
    pyplot.xlabel("x")
    pyplot.ylabel("y")
    pyplot.title("Quadratic Function")
    pyplot.grid(True)
    pyplot.show()
    pyplot.clf()
