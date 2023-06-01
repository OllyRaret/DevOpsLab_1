import math
import os.path
import numpy as np


def function1(a: float, b: float, n: int):
    function_name = 'sin(x)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [math.sin(i) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function2(a: float, b: float, n: int):
    function_name = 'cos(x)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [math.cos(i) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function3(a: float, b: float, n: int):
    function_name = '(sin^2(x - 7)-x^(2))/3'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [((math.sin(i - 7) ** 2 - i ** 2) / 3) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function4(a: float, b: float, n: int):
    function_name = '(3x + 3)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [(3 * i + 3) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function5(a: float, b: float, n: int):
    function_name = '(sin(x) - x^3)/2)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [(math.sin(i) - i / 2) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function6(a: float, b: float, n: int):
    function_name = '(exp(x+3))'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [(math.exp(i + 3) for i in x)]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function7(a: float, b: float, n: int):
    function_name = 'sin^2(x)-4sin(x)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [math.sin(i) ** 2 - 4 * math.sin(i) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function8(a: float, b: float, n: int):
    f_name = '1/(x ** 2 + 2)'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [1 / ((i ** 2) + 2) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def function9(a: float, b: float, n: int):
    f_name = '(x + 5) + 25 / 6'
    dx = (b - a) / (n - 1)
    x = [a + i * dx for i in range(n)]
    y = [((i + 5) + 25 / 6) for i in x]
    points: list = [[x[i], y[i]] for i in range(n)]
    return function_name, points


def write_to_file(f_num: int, a: float, b: float, n: int):
    f_name = ''
    match f_num:
        case 1:
            f_name, points = function1(a, b, n)
        case 2:
            f_name, points = function2(a, b, n)
        case 3:
            f_name, points = function3(a, b, n)
        case 4:
            f_name, points = function4(a, b, n)
        case 5:
            f_name, points = function5(a, b, n)
        case 6:
            f_name, points = function6(a, b, n)
        case 7:
            f_name, points = function7(a, b, n)
        case 8:
            f_name, points = function8(a, b, n)
        case 9:
            f_name, points = function9(a, b, n)
    if f_name == '':
        return

    f = open(f'f{f_num}.txt', "w")
    f.write(f_name + '\n')
    f.writelines(str(p).replace('[', '').replace(']', '').replace(',', '') + '\n' for p in points)

    f.close()


def read_from_file(f_num):
    if not os.path.exists(f'f{f_num}.txt'):
        return '', []
    f = open(f'f{f_num}.txt', "r")
    f_name = f.readline()

    p = f.readlines()
    f.close()
    points = [list(map(float, c.split())) for c in p]
    x = [c[1] for c in points]
    return f_name, x
