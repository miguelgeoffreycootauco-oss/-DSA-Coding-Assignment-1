import csv
import math
import random
from pathlib import Path

from mergesort import merge_sort
from search import load_titles, binary_search

TRIALS = 30
SEED = 30
MAX_N = 500
OUTPUT = Path(__file__).with_name('benchmark_results.csv')


def worst_order(values):
    # Arrange sorted values to interleave at each merge 

    if len(values) <= 1:
        return values[:]
    return worst_order(values[1::2]) + worst_order(values[::2])


def best_count(n):
    if n <= 1:
        return 0
    left = n // 2
    return best_count(left) + best_count(n - left) + left


def worst_count(n):
    if n <= 1:
        return 0
    levels = math.ceil(math.log2(n))
    return n * levels - 2 ** levels + 1


def measure_sort(values, expected):
    stats = {'comparisons': 0}
    result = merge_sort(values[:], stats, trace=False)
    if result != expected:
        raise AssertionError('Merge Sort returned incorrect output')
    return stats['comparisons']


def measure_search(values, target, should_find):
    stats = {'steps': 0}
    index = binary_search(values, target, stats)
    if should_find:
        if index < 0 or values[index] != target:
            raise AssertionError('Binary Search missed an existing title')
    elif index != -1:
        raise AssertionError('Binary Search found a nonexistent title')
    return stats['steps']


def add_row(rows, n, algorithm, case, metric, counts, reference, note):
    rows.append({
        'n': n, 'algorithm': algorithm, 'case': case, 'metric': metric,
        'runs': len(counts), 'mean_count': sum(counts) / len(counts),
        'min_count': min(counts), 'max_count': max(counts),
        'reference_count': reference, 'note': note,
    })


def benchmark(titles):
    rows = []
    limit = min(MAX_N, len(titles))
    if limit < 10:
        raise ValueError('At least 10 usable titles are needed.')
    sizes = list(range(10, limit + 1, 10))
    if sizes[-1] != limit:
        sizes.append(limit)

    for n in sizes:

        sample = titles[:n]
        setup_stats = {'comparisons': 0}
        ordered = merge_sort(sample[:], setup_stats)
        if ordered != sorted(sample):

            raise AssertionError('Incorrect setup ordering')

        best = measure_sort(ordered, ordered)
        if best != best_count(n):
            raise AssertionError('Best-case comparison count did not match')
        add_row(rows, n, 'MergeSort', 'best', 'element_comparisons',
                [best], best_count(n), 'Sorted ascending; verified minimum')

        rng = random.Random(SEED + n)
        counts = []
        for trial in range(TRIALS):
            shuffled = sample[:]
            rng.shuffle(shuffled)
            counts.append(measure_sort(shuffled, ordered))
        add_row(rows, n, 'MergeSort', 'average_estimate',
                'element_comparisons', counts, '',
                f'Mean of {TRIALS} seeded shuffles; seed={SEED}+n')

        worst = measure_sort(worst_order(ordered), ordered)
        bound = worst_count(n)
        if worst > bound:
            raise AssertionError('Comparison count exceeds upper bound')
        verified = worst == bound
        add_row(rows, n, 'MergeSort', 'worst' if verified else 'worst_candidate',
                'element_comparisons', [worst], bound,
                'Interleaved input; upper bound attained' if verified else
                'Duplicates: constructed input did not attain general upper bound')

        midpoint = ordered[(n - 1) // 2]
        best = measure_search(ordered, midpoint, True)
        add_row(rows, n, 'BinarySearch', 'best', 'midpoint_probes', [best], 1,
                'Target is the first midpoint')
        counts = [measure_search(ordered, title, True) for title in ordered]
        add_row(rows, n, 'BinarySearch', 'average_successful', 'midpoint_probes',
                counts, '', 'Mean across all n records; repeated titles retain their weight')
        
        # A string extending the largest title sorts strictly after it.
        # This follows the deepest right path: floor(log2(n)) + 1 probes.
        
        missing = ordered[-1] + '\0'
        worst = measure_search(ordered, missing, False)
        bound = n.bit_length()
        if worst != bound:
            raise AssertionError('Worst-case search count did not match')
        add_row(rows, n, 'BinarySearch', 'worst_unsuccessful', 'midpoint_probes',
                [worst], bound, 'Absent target after largest title; verified maximum')
    return rows


def main():
    titles = load_titles()
    print(f'Usable titles: {len(titles)}; distinct titles: {len(set(titles))}')
    if len(titles) < MAX_N:
        print(f'Only {len(titles)} records available: sizes above this are skipped, not fabricated.')
    rows = benchmark(titles)
    with OUTPUT.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Saved {len(rows)} summary rows to {OUTPUT.name}')
    print('\nFinal input size:')
    for row in rows[-6:]:
        print(f"{row['algorithm']:12} {row['case']:22} "
              f"{row['mean_count']:10.2f} {row['metric']}")


if __name__ == '__main__':
    main()
