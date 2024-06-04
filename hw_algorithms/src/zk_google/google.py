import re
import string
import random

from itertools import combinations

def generate_substrings(s):
    substrings = []
    n = len(s)
    for length in range(1, n + 1):
        substrings.extend([''.join(comb) for comb in combinations(s, length)])
    ret = []
    for i in range(len(substrings)):
        ret.append([])
        ret[i].append(substrings[i])
    return ret


def z_algorithm(s):
    n = len(s)
    z_values = [0] * n

    z_values[0] = n

    L, R = 0, 0

    for i in range(1, n):
        if i <= R:
            z_values[i] = min(R - i + 1, z_values[i - L])

        while i + z_values[i] < n and s[z_values[i]] == s[i + z_values[i]]:
            z_values[i] += 1

        if i + z_values[i] - 1 > R:
            L, R = i, i + z_values[i] - 1

    return z_values

def count_substring_occurrences(main_string, substring):
    combined_string = substring + "$" + main_string
    z_values = z_algorithm(combined_string)
    substring_length = len(substring)
    count = 0

    for i in range(len(z_values)):
        if z_values[i] == substring_length:
            count += 1

    return count


if __name__ == '__main__':
    n_cases = int(input())

    for _ in range(n_cases):
        n_documents, n_queries = tuple(map(int, input().split()))
        # num_documents, num_queries = int(temp[0]), int(temp[1])
        documents = [input() for i in range(n_documents)]
        queries = [input().split()[1:] for i in range(n_queries)]

        for query in queries:
            matches = []
            for index, document in enumerate(documents, start=1):
                matches.append((index, sum([count_substring_occurrences(document, word) for word in query])))

            matches = sorted(matches, key=lambda k: k[1], reverse=True)
            if matches[0][1] == 0:
                print("No document found.")
                print()
                continue
            for doc_num,match in matches:
                if match > 0:
                    if match == 1:
                        print(f"Document {doc_num}: {match} match")
                    else:
                        print(f"Document {doc_num}: {match} matches")

            print()
