def fib_gen(n):
    current, next = 0, 1
    for _ in range(0, n+1):
        yield current
        current, next = next, current+next


def fib(int_str):
    result = 0
    for result in fib_gen(int(int_str)):
        pass
    return result

