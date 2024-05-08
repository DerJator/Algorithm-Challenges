def shift_lowercase_ascii(text, n):
    shifted_text = []
    for char in text:
        shifted_char = chr(((ord(char) - 97 + n) % 26) + 97)
        shifted_text.append(shifted_char)
    return ''.join(shifted_text)

if __name__ == '__main__':
    reference_mask = [3, 5, 5, 3, 5, 4, 3, 4, 3]  # word lengths, implicit space in between
    space_pos = [3, 9, 15, 19, 25, 30, 34, 39, 43]
    reference_str = "the quick brown fox jumps over the lazy dog"
    # Duplicates and positions in reference string:
    duplicates = {'e': [2, 28, 33], 'h': [1, 32], 'o': [12, 17, 26, 41], 'r': [11, 29], 't': [0, 31], 'u': [5, 21]}

    eof_flag = False
    n_cases = int(input())
    input()  # Skip empty first line
    for testcase in range(n_cases):
        if eof_flag:
            break

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

        """" Find possible reference string """
        ref_line = -1

        for l2, line in enumerate(lines):
            ctr = 0
            ref_ix = 0
            mismatch_flag = False

            # Search for the reference string
            if len(line) != len(reference_str):
                continue

            space_ctr = 0
            for c_ix, c in enumerate(line):
                if c_ix == space_pos[space_ctr]:
                    if c != ' ':
                        mismatch_flag = True
                        break
                    else:
                        space_ctr += 1
                elif c_ix != space_pos[space_ctr] and c == ' ':
                    mismatch_flag = True
                    break

            # First matching line: Build up letter mapping
            # Watch out for consistent mapping
            if not mismatch_flag:
                ref_dict = {' ': ' '}
                ref_line = l2
                space_ctr = 0
                # print(f"Reference string could be in line {ref_line}")
                for c_ix, c in enumerate(line):
                    # print(f"{c}->{reference_str[c_ix]}")
                    # Check if the character has already been mapped, if so check if the duplicate is at an allowed
                    # position (duplicates in the reference string)
                    if c in ref_dict.keys():
                        if not c == ' ':
                            # print(f"Duplicate letter: {c}")
                            try:
                                # print(f"'{reference_str[c_ix]}'")
                                # print(f"{duplicates[reference_str[c_ix]]}")
                                # print(f"{c_ix=}")

                                # Check if the position of the reference string allows a duplicate
                                if c_ix not in duplicates[reference_str[c_ix]][1:]:
                                    ref_line = -1
                                    break

                                if ref_dict[c] != reference_str[c_ix]:
                                    # print("Allowed Duplicate, but ambiguous mapping")
                                    ref_line = -1
                                    break

                            except KeyError:
                                # print("KeyError")
                                ref_line = -1
                                break

                    if c == ' ':
                        pass
                    ref_dict[c] = reference_str[c_ix]
                if ref_line != -1:  # String matched reference string!
                    # print(f"Reference string match in {ref_line}")
                    break
                elif l2 == len(lines) - 1:  # Last possibility, so no solution, else continue finding reference string
                    # print("No solution because last string didn't match")
                    ref_line = -1

        if ref_line == -1:
            print("No solution.")
            print("")
            continue

        """ Decryption Party """
        # Decrypt all lines

        no_solution = False
        solutions = []
        for l3, line in enumerate(lines):
            if l3 == ref_line:
                solutions.append(reference_str)
                continue
            decryption = ['x'] * len(line)
            for ix, char in enumerate(line):
                try:
                    decryption[ix] = ref_dict[char]
                except KeyError:
                    no_solution = True
                    # print("No solution.")
                    break

            if no_solution:
                print("No solution.")
                break
            else:
                solutions.append("".join(decryption))

        if not no_solution:
            print("\n".join(solutions))

        print()
