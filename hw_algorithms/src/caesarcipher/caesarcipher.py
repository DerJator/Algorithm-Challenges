import string

alphabet_dict = {letter: index for index, letter in enumerate(string.ascii_uppercase)}
alpha_by_ix = {index: letter for index, letter in enumerate(string.ascii_uppercase)}


def mfq_letter(text: str):
    letter_hist = {}

    for char in text:
        if char != ' ':
            letter_hist[char] = letter_hist.get(char, 0) + 1

    hist = letter_hist.values()
    mx = 0
    mx_count = 0  # number of elements with max val
    for i, v in enumerate(hist):
        if v > mx:
            mx = v
            argmax = i
            mx_count = 0
        if v == mx:
            mx_count += 1

    if mx_count == 1:
        return list(letter_hist.keys())[argmax]
    else:
        return -1


def decrypt(text: str, offset: int):
    decrypted = []
    for char in text:
        if char != ' ':
            char_ix = alphabet_dict[char]
            decrypted.append(alpha_by_ix[(char_ix - offset) % 26])
        else:
            decrypted.append(' ')

    return ''.join(decrypted)


if __name__ == '__main__':
    n_iter = int(input())

    for l in range(n_iter):
        text = input()
        mfq = mfq_letter(text)
        if mfq == -1:
            print("NOT POSSIBLE")
            continue

        letter_diff = (26 + alphabet_dict.get(mfq) - 4) % 26
        print(letter_diff, decrypt(text, letter_diff))
