"""Optional validation: python test_benchmark.py (not part of timed results)."""
import itertools
from benchmark import benchmark, best_count, worst_count, worst_order, measure_sort
from mergesort import merge_sort
from search import binary_search

for n in range(8):
    expected = list(range(n))
    counts = [measure_sort(list(p), expected) for p in itertools.permutations(expected)]
    assert min(counts) == best_count(n)
    assert max(counts) == worst_count(n)
    assert measure_sort(worst_order(expected), expected) == max(counts)
for values in [[], ['a'], ['z', 'a', 'a'], ['a'] * 10]:
    stats = {'comparisons': 0}
    ordered = merge_sort(values[:], stats)
    assert ordered == sorted(values)
    for target in values + ['missing']:
        s = {'steps': 0}
        i = binary_search(ordered, target, s)
        assert (i == -1) == (target not in ordered)
        if i != -1:
            assert ordered[i] == target
sample = [f'Title {i:02}' for i in range(25)]
a = benchmark(sample)
assert a == benchmark(sample)
assert sorted(set(r['n'] for r in a)) == [10, 20, 25]
assert len(a) == 18
assert any(r['case'] == 'worst_candidate' for r in benchmark(['same'] * 10))
print('PASS: exhaustive permutations n=0..7, duplicate/empty/singleton cases, search correctness, reproducibility, size cap, duplicate worst-case labeling.')
