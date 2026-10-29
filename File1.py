### Binary Search with Step Counter

"""
Binary search over the Top 500 Movies CSV.

Binary search only works on SORTED data, so each search first makes sure the
column is sorted (Rank already is; Title and Year are sorted on demand).

Because Title and Year can repeat (e.g. remakes), the search uses
lower-bound / upper-bound variants so it returns ALL matching rows, not
just one arbitrary hit.
"""

import pandas as pd

import os

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Top_500_Movies_Ranked_by_Combined_Critics_and_Audience_Scores.csv",
)


# --------------------------------------------------------------------------
# Core binary search routines (work on any sorted list)
# --------------------------------------------------------------------------

### Same as the slides
def binary_search(sorted_values, target):
    """Classic binary search. Returns an index of target, or -1 if absent."""
    low, high = 0, len(sorted_values) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_values[mid] == target:
            return mid
        elif sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def lower_bound(sorted_values, target):
    """First index i where sorted_values[i] >= target."""
    low, high = 0, len(sorted_values)
    while low < high:
        mid = (low + high) // 2
        if sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low

def upper_bound(sorted_values, target):
    """First index i where sorted_values[i] > target."""
    low, high = 0, len(sorted_values)
    while low < high:
        mid = (low + high) // 2
        if sorted_values[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low


# --------------------------------------------------------------------------
# Search helpers for the movie data
# --------------------------------------------------------------------------
def load_movies(path=CSV_PATH):
    return pd.read_csv(path)


def search_by_rank(df, rank):
    """Find a movie by its exact Rank. Rank is unique and already sorted."""
    ranks = df["Rank"].tolist()
    idx = binary_search(ranks, rank)
    return df.iloc[idx] if idx != -1 else None


def search_by_title(df, title):
    """Find all movies with this exact title (case-insensitive)."""
    # Title is NOT sorted in the file, so sort a copy by lowercase title.
    sorted_df = (
        df.assign(_key=df["Title"].str.lower())
        .sort_values("_key", kind="stable")
        .reset_index(drop=True)
    )
    keys = sorted_df["_key"].tolist()
    target = title.lower()
    lo, hi = lower_bound(keys, target), upper_bound(keys, target)
    return sorted_df.iloc[lo:hi].drop(columns="_key")


def search_by_year_range(df, start_year, end_year):
    """Find all movies released between start_year and end_year (inclusive)."""
    sorted_df = df.sort_values("Year", kind="stable").reset_index(drop=True)
    years = sorted_df["Year"].tolist()
    lo, hi = lower_bound(years, start_year), upper_bound(years, end_year)
    return sorted_df.iloc[lo:hi]


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------
if __name__ == "__main__":
    movies = load_movies()
    show = ["Rank", "Title", "Year", "Director", "IMDb_10", "Custom_Score"]

    print("--- Search by Rank (rank = 7) ---")
    row = search_by_rank(movies, 7)
    print(row[show] if row is not None else "Not found")

    print("\n--- Search by Title ('pulp fiction') ---")
    result = search_by_title(movies, "pulp fiction")
    print(result[show] if not result.empty else "Not found")

    print("\n--- Search by Year range (1950-1955) ---")
    result = search_by_year_range(movies, 1950, 1955)
    print(result[show].to_string(index=False))
