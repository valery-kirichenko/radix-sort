import random
import time
import sys
import json
import math
import matplotlib.pyplot as plt
from operator import itemgetter

import algorithm


def generate(length, amount):
    return [random.randint(length, 10 * length - 1) for _ in range(amount)]


def timer(length, amount, number=2000):
    times = []
    for _ in range(number):
        to_sort = generate(length, amount)
        start = time.time()
        algorithm.radix_sort(to_sort, 10)
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
            print(f'Testing arrays with {amount} elements from {length} '
                  f'to {10 * length - 1}')
            ex_time = timer(length, amount)
            tested.append({'from': length,
                           'to': 10 * length,
                           'amount': amount,
                           'time': ex_time * 1000})
            print(f'{ex_time * 1000}ms')
    return tested


if 'load' in sys.argv:
    with open('results.txt') as results_file:
        test_results = json.loads(results_file.read())
else:
    test_results = test()
    with open('results.txt', 'w') as f:
        f.write(json.dumps(test_results))


amount_series = list(chunks(list(range(len(amounts) * len(lengths))), len(amounts)))
length_series = [[x + i for x in list(range(0, len(amounts) * len(lengths), len(amounts)))] for i in range(len(amounts))]

plt.figure(1)
plt.title('Зависимость от числа элементов')
plt.xlabel('Число элементов')
plt.ylabel('Время выполнения (мс)')
plt.grid(True)
# {a -> 0.000519248, b -> 0.851639, c -> 1.01574, d -> 0.30329}
for amount_indices in amount_series:
    plt.plot([test_result['amount'] for test_result in itemgetter(*amount_indices)(test_results)],
        [test_result['time'] for test_result in itemgetter(*amount_indices)(test_results)],
        label=f'{len(str(test_results[amount_indices[0]]["from"]))}', marker='.')
plt.plot(amounts, [0.000519248 * 8**0.851639 * amount**1.01574 + 0.30329 for amount in amounts], '--', label='Аппроксимация для 8')
plt.legend(title='Количество разрядов')
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
plt.plot([len(str(length)) for length in lengths], [0.000519248 * len(str(length))**0.851639 * 51200**1.01574 + 0.30329 for length in lengths], '--', label='Аппроксимация\nдля 52000')
plt.legend(title='Число элементов', loc='center', bbox_to_anchor=(1.27, 0.5), ncol=2)
plt.savefig('length.png', bbox_inches='tight', dpi=300)
plt.xscale('log')
plt.yscale('log')
plt.savefig('length_log.png', bbox_inches='tight', dpi=300)
# plt.show()
