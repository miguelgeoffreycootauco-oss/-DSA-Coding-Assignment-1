def merge_sort(arr, stats, trace=False, depth=0):
    indent = "    " * depth

    if len(arr) <= 1:
        if trace:
            print(f"{indent}base case: {arr}")
        return arr

    mid = len(arr) // 2
    if trace:
        print(f"{indent}split: {arr} -> {arr[:mid]} | {arr[mid:]}")

    left = merge_sort(arr[:mid], stats, trace, depth + 1)
    right = merge_sort(arr[mid:], stats, trace, depth + 1)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        stats["comparisons"] += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged += left[i:]
    merged += right[j:]

    if trace:
        print(f"{indent}merge: {left} + {right} -> {merged}")
    return merged


if __name__ == "__main__":
    sample = ["The Godfather", "Seven Samurai", "12 Angry Men", "Schindler's List",
              "The Godfather: Part II", "Rear Window", "Pulp Fiction", "City Lights",
              "Spirited Away", "Parasite"]
    stats = {"comparisons": 0}
    result = merge_sort(sample, stats, trace=True)
    print("\nSorted:", result)
    print("Comparisons:", stats["comparisons"])

    for case in ([], ["a"], [2, 1], [3, 3, 3], [1, 2, 3], [3, 2, 1]):
        s = {"comparisons": 0}
        assert merge_sort(list(case), s) == sorted(case), case
    print("Edge cases passed")
