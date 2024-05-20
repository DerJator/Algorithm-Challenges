class Permutator:
    def __init__(self, m, k):
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.usable_alphabet = []
        self.max_len = m
        self.k = k
        self.permute_ix = None
        self.terminated = False
        self.reset_params(m, k)

    def reset_params(self, m, k):
        self.max_len = m
        self.k = k
        self.permute_ix = [0 for _ in range(m)]
        self.usable_alphabet = self.alphabet[:k]
        self.terminated = False

    def next_permutation(self):
        if not self.terminated:
            perm = ''.join([self.usable_alphabet[j] for j in self.permute_ix])
            self.k_add()
            return perm
        else:
            return None

    def k_add(self):
        self.permute_ix[-1] += 1

        for i in range(1, m+1):
            if self.permute_ix[-i] % k == 0 and self.permute_ix[-i] != 0:
                if i < m:
                    self.permute_ix[-i] = 0
                    self.permute_ix[-(i+1)] += 1
                else:
                    self.terminated = True
                    return


def schnipsel(doc):
    schnipsels = set()
    for i in range(len(doc) - m + 1):
        schnipsels.add(doc[i:i + m])

    schnipsels = sorted(schnipsels)

    return schnipsels


if __name__ == '__main__':
    n_cases = int(input().strip())
    permutator = Permutator(0, 0)

    for case in range(n_cases):
        # n: doc length, m: max query length, k: letters 1..k
        n, m, k = map(int, input().strip().split(' '))
        doc_string = input().strip()
        permutator.reset_params(m, k)

        doc_schnipsel = schnipsel(doc_string)
        # Fill missing values with certain non-match, s.t. iteration can go to k^m

        for i in range(k**m):
            perm = permutator.next_permutation()
            if i >= len(doc_schnipsel):
                print(perm)
                break
            if doc_schnipsel[i] != perm:
                print(perm)
                break
