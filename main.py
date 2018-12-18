import random
import time
import json
import math
import matplotlib.pyplot as plt
from operator import itemgetter

import algorithm


def generate(length, amount):
    return [random.randint(length, 10 * length - 1) for _ in range(amount)]


def timer(f, *args, number=1000):
    times = []
    for _ in range(number):
        start = time.time()
        f(*args)
        stop = time.time()
        times.append(stop - start)
    return sum(times) / number


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


lengths = [1, 10, 1000, 10000000]
amounts = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]

def test():
    tested = list()
    for length in lengths:
        for amount in amounts:
            print(f'Testing arrays with {amount} elements from {length} to {10 * length - 1}')
            to_sort = generate(length, amount)
            ex_time = timer(algorithm.radix_sort, to_sort, 10)
            tested.append({'from': length,
                           'to': 10 * length,
                           'amount': amount,
                           'time': ex_time * 1000})
            print(f'{ex_time * 1000}ms')
    return tested


test_results = test()
with open('results.txt', 'w') as f:
    f.write(json.dumps(test_results))
"""
test_results = [{'from': 100, 'to': 1000, 'amount': 100, 'time': 0.2936387062072754},
 {'from': 100, 'to': 1000, 'amount': 1000, 'time': 2.571721076965332},
 {'from': 100, 'to': 1000, 'amount': 10000, 'time': 25.2116060256958},
 {'from': 100, 'to': 1000, 'amount': 50000, 'time': 132.6355004310608},
 {'from': 100, 'to': 1000, 'amount': 100000, 'time': 303.45458030700684},
 {'from': 1000, 'to': 10000, 'amount': 100, 'time': 0.39357900619506836},
 {'from': 1000, 'to': 10000, 'amount': 1000, 'time': 3.5889291763305664},
 {'from': 1000, 'to': 10000, 'amount': 10000, 'time': 33.23658227920532},
 {'from': 1000, 'to': 10000, 'amount': 50000, 'time': 179.6462917327881},
 {'from': 1000, 'to': 10000, 'amount': 100000, 'time': 409.38971519470215},
 {'from': 10000, 'to': 100000, 'amount': 100, 'time': 0.49304246902465815},
 {'from': 10000, 'to': 100000, 'amount': 1000, 'time': 4.22809362411499},
 {'from': 10000, 'to': 100000, 'amount': 10000, 'time': 44.155919551849365},
 {'from': 10000, 'to': 100000, 'amount': 50000, 'time': 238.2860016822815},
 {'from': 10000, 'to': 100000, 'amount': 100000, 'time': 492.75259733200073},
 {'from': 100000, 'to': 1000000, 'amount': 100, 'time': 0.5645918846130371},
 {'from': 100000, 'to': 1000000, 'amount': 1000, 'time': 5.214958190917969},
 {'from': 100000, 'to': 1000000, 'amount': 10000, 'time': 50.919528007507324},
 {'from': 100000, 'to': 1000000, 'amount': 50000, 'time': 289.8490285873413},
 {'from': 100000, 'to': 1000000, 'amount': 100000, 'time': 590.8728098869324}]
"""

amount_series = list(chunks(list(range(len(amounts) * len(lengths))), len(amounts)))
length_series = [[x + i for x in list(range(0, len(amounts) * len(lengths), len(amounts)))] for i in range(len(lengths) + 1)]

plt.figure(1)
plt.title('Зависимость от числа элементов')
plt.xlabel('Число элементов')
plt.ylabel('Время выполнения (мс)')
plt.grid(True)
for amount_indices in amount_series:
    plt.plot([test_result['amount'] for test_result in itemgetter(*amount_indices)(test_results)],
        [test_result['time'] for test_result in itemgetter(*amount_indices)(test_results)],
        label=f'{test_results[amount_indices[0]]["from"]}-{test_results[amount_indices[0]]["to"]}', marker='.')
plt.legend(title='Диапазон чисел')
plt.savefig('amount.png', bbox_inches='tight', dpi=300)
plt.xscale('log')
plt.yscale('log')
plt.savefig('amount_log.png', bbox_inches='tight', dpi=300)

plt.figure(2)
plt.title('Зависимость от длины чисел')
plt.xlabel('Длина числа')
plt.ylabel('Время выполнения (мс)')
plt.grid(True)
for length_indices in length_series:
    plt.plot([math.log(test_result['to'], 10) for test_result in itemgetter(*length_indices)(test_results)],
        [test_result['time'] for test_result in itemgetter(*length_indices)(test_results)],
        label=test_results[length_indices[0]]['amount'], marker='.')
plt.legend(title='Число элементов')
plt.savefig('length.png', bbox_inches='tight', dpi=300)
plt.xscale('log')
plt.yscale('log')
plt.savefig('length_log.png', bbox_inches='tight', dpi=300)
# plt.show()
