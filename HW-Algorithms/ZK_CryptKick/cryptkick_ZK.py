def shift_lowercase_ascii(text, n):
    shifted_text = []
    for char in text:
        shifted_char = chr(((ord(char) - 97 + n) % 26) + 97)
        shifted_text.append(shifted_char)
    return ''.join(shifted_text)

if __name__ == '__main__':
    reference_mask = [3, 5, 5, 3, 5, 4, 3, 4, 3]  # word lengths, implicit space in between
    reference_str = "the quick brown fox jumps over the lazy dog"

    eof_flag = False
    n_cases = int(input())
    input()  # Skip empty first line
    for testcase in range(n_cases):
        if eof_flag:
            break

        ref_dict = {' ': ' '}

        """ Read in all lines """
        lines = []
        for l in range(100):
            try:
                line = input()
            except EOFError:
                break
            if line == "" or line == "\n":
                break

            lines.append(line)  # Save for decryption

        """" Find reference string """
        ref_line = -1
        for l2, line in enumerate(lines):
            ctr = 0
            ref_ix = 0
            mismatch_flag = False

            # Search for the reference string
            for c in line:
                if c != ' ':
                    ctr += 1
                else:
                    if reference_mask[ref_ix] != ctr:
                        mismatch_flag = True
                    ctr = 0
                    if mismatch_flag:
                        break
                    ref_ix += 1

            # First matching line: Build up letter mapping
            if not mismatch_flag:
                ref_line = l2
                for i, c in enumerate(line):
                    ref_dict[c] = reference_str[i]
                break

        if ref_line == -1:
            print("No solution.\n")
            continue

        """ Decryption Party """
        # Decrypt all lines

        no_solution = False
        for l3, line in enumerate(lines):
            if l3 == ref_line:
                print(reference_str)
                continue
            decryption = ['x'] * len(line)
            for ix, char in enumerate(line):
                try:
                    decryption[ix] = ref_dict[char]
                except KeyError:
                    no_solution = True
                    print("No solution.")
                    break

            if not no_solution:
                print("".join(decryption))

        print()
