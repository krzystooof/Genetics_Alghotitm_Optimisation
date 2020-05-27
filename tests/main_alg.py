import pyb.src.algorithm

def function(x):
    # x^2 + 3x +7
    return x[0] * x[0] + x[0] * 3 + 7

alg = Algorithm(function, values = 1, population = 100, generations = 15, rand_low = -100, rand_high = 100, reverse = True)

result = agl.run()
print("This function has a minimum of: " + str(result))
