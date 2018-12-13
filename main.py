import random
import time

import algorithm


def timer(f, *args, number=1000):
    times = []
    for _ in range(number):
        start = time.time()
        f(*args)
        stop = time.time()
        times.append(stop - start)
    return sum(times) / number


def test():
    to_sort = [random.randint(100, 10000) for r in range(10000)]
    tested = list()

    for length in range(2, 6):
        for amount in range(2, 6):
            print(f'Testing arrays with {10 ** amount} elements from {10 ** length} to {10 ** (length + 1)}')
            to_sort = [random.randint(10 ** length, 10 ** (length + 1) - 1)
                       for _ in range(10 ** amount)]
            ex_time = timer(algorithm.radix_sort, to_sort, 10)
            tested.append({'range': f'{10 ** length}-{10 ** (length + 1) - 1}',
                           'amount': 10 ** amount,
                           'time': f'{ex_time * 1000}ms'})
            print(f'{ex_time * 1000}ms')
    return tested

test_results = test()
print(test_results)
