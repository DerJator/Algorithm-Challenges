# TODO TIMELIMIT
import collections
import functools


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


def levenshtein_timelimit(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


@memoized
def editDistance(str1, str2, m, n):

    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m-1] == str2[n-1]:
        return editDistance(str1, str2, m-1, n-1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(editDistance(str1, str2, m, n-1),    # Insert
                   editDistance(str1, str2, m-1, n),    # Remove
                   editDistance(str1, str2, m-1, n-1)    # Replace
                   )


def minDis(s1, s2, n, m, dp):
    # Time Complexity: O(m x n)
    # Auxiliary Space: O( m *n)+O(m+n) , (m*n) extra array space and (m+n) recursive stack space.

    # n = len(str1)
    # m = len(str2)
    # dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
    # If any string is empty,
    # return the remaining characters of other string
    if n == 0:
        return m
    if m == 0:
        return n

    # To check if the recursive tree
    # for given n & m has already been executed
    if(dp[n][m] != -1):
        return dp[n][m]

    # If characters are equal, execute
    # recursive function for n-1, m-1
    if(s1[n - 1] == s2[m - 1]):
        if(dp[n - 1][m - 1] == -1):
            dp[n][m] = minDis(s1, s2, n - 1, m - 1, dp)
            return dp[n][m]
        else:
            dp[n][m] = dp[n - 1][m - 1]
            return dp[n][m]

    # If characters are nt equal, we need to
    # find the minimum cost out of all 3 operations.
    else:
        if(dp[n - 1][m] != -1):
            m1 = dp[n - 1][m]
        else:
            m1 = minDis(s1, s2, n - 1, m, dp)

        if(dp[n][m - 1] != -1):
            m2 = dp[n][m - 1]
        else:
            m2 = minDis(s1, s2, n, m - 1, dp)
        if(dp[n - 1][m - 1] != -1):
            m3 = dp[n - 1][m - 1]
        else:
            m3 = minDis(s1, s2, n - 1, m - 1, dp)

        dp[n][m] = 1 + min(m1, min(m2, m3))
        return dp[n][m]


def editDistance(s: str, t: str) -> int:
    # Time Complexity: O(M x N) where M and N are lengths of the string
    # Auxiliary Space: O( N ), Length of the str2
    n = len(s)
    m = len(t)

    prev = [j for j in range(m+1)]
    curr = [0] * (m+1)

    for i in range(1, n+1):
        curr[0] = i
        for j in range(1, m+1):
            if s[i-1] == t[j-1]:
                curr[j] = prev[j-1]
            else:
                mn = min(1 + prev[j], 1 + curr[j-1])
                curr[j] = min(mn, 1 + prev[j-1])
        prev = curr.copy()

    return prev[m]

num_tc = int(input())

for _ in range(num_tc):
    word = input()
    n_words = int(input())

    possible_matches = []
    for i in range(n_words):
        possible_matches.append(input())

    # possible_matches = get_close_matches(word, possible_matches, 10)  # nope

    curr_lowest_dist = 10000000 # some high number to initialize
    curr_match = ""
    for m in possible_matches:
        # dist = levenshtein(word, m)
        # n = len(word)
        # m_len = len(m)
        # dp = [[-1 for i in range(m_len + 1)] for j in range(n + 1)]
        # dist = minDis(word, m, n, m_len, dp)
        dist = editDistance(word, m)

        if dist < curr_lowest_dist:
            curr_lowest_dist = dist
            curr_match = m

    print(f"best match for '{word}' is '{curr_match}' with score {curr_lowest_dist}")
