# Generador Fibonacci con yield
def fib(limit):
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

print(list(fib(20)))
