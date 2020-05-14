def test_quadratic_function():
    print("Give a, b and c")
    a = input()
    b = input()
    c = input()

    a = int(a)
    b = int(b)
    c = int(c)
    if a == 0:
        if b != 0:
            print("This function doesn't have minimum or maximum")
        else:
            print(f'Minimum of this function is: {c}')
    if a < 0:
        delta = (b * b) - (4 * a * c)
        maximum_x = (-b) / (2 * a)
        maximum_y = (-delta) / (4 * a)
        print(f'This function has maximum in point x= {maximum_x}')
    if a > 0:
        delta = (b * b) - (4 * a * c)
        minimum_x = (-b) / (2 * a)
        minimum_y = (-delta) / (4 * a)
        print(f'This function has minimum in point x= {minimum_x}')


def test_function():
    x_3 = 1
    x_2 = 6
    x_1 = 9
    x = -3
    print(f'f(x)= x^3+{x_2}x^2+{x_1}x{x}')
    print("derivative of a function")
    x_3 = x_3 * 3
    x_2 = x_2 * 2
    x_1 = x_1
    x = 0
    print(f'f`(x)= {x_3}x^2+{x_2}x+{x_1} = 3(x+1)(x+3)')
    print(f'x1 = -1 v x2 = -3')
    print(f'Maximum: f(-3) = -3')
    print(f'Minimum: f(-1) = -7')
    print('>> X = -7')
