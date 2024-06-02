if __name__ == '__main__':
    n_iter = int(input())

    for l in range(n_iter):
        text = input()
        dict_hist = {}
        for char in text:
            dict_hist[char] = dict_hist.get(char, 0) + 1

        hist = dict_hist.values()
        argmax = -1
        mx = 0
        for i, v in enumerate(hist):
            if v > mx:
                argmax = i
