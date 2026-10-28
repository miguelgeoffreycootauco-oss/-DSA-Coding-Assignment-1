import os

import pandas as pd

from mergesort import merge_sort

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Top_500_Movies_Ranked_by_Combined_Critics_and_Audience_Scores.csv",
)


def binary_search(sorted_values, target, stats=None):
    low, high = 0, len(sorted_values) - 1
    while low <= high:
        if stats is not None:
            stats["steps"] += 1
        mid = (low + high) // 2
        if sorted_values[mid] == target:
            return mid
        elif sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def load_titles(path=CSV_PATH):
    df = pd.read_csv(path)
    print(len(df), "rows loaded")
    return df["Title"].dropna().astype(str).str.strip().tolist()


if __name__ == "__main__":
    titles = load_titles()
    sort_stats = {"comparisons": 0}
    sorted_titles = merge_sort(titles, sort_stats)
    print("MergeSort comparisons:", sort_stats["comparisons"])

    for target in ["Pulp Fiction", "Not A Real Movie"]:
        search_stats = {"steps": 0}
        idx = binary_search(sorted_titles, target, search_stats)
        print(f"'{target}': index {idx}, steps {search_stats['steps']}")
