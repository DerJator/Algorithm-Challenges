reference_mask = [3, 5, 5, 3, 5, 4, 3, 4, 3]  # word lengths, implicit space in between
space_pos = {3, 9, 15, 19, 25, 30, 34, 39}
reference_str = "the quick brown fox jumps over the lazy dog"

# Duplicates and positions in reference string:
duplicates = {'e': [2, 28, 33], 'h': [1, 32], 'o': [12, 17, 26, 41], 'r': [11, 29], 't': [0, 31], 'u': [5, 21]}
duplicates_by_pos = {0: [31], 1: [32], 2: [28, 33], 5: [21], 11: [29], 12: [17, 26, 41]}  # for the first letter occurence

def is_bijective_mapping(string):
    mapping = {}
    mapped_letters = set()

    for i in range(len(reference_str)):
        ref_char = reference_str[i]
        string_char = string[i]

        if ref_char in mapping:
            if mapping[ref_char] != string_char:
                return False
        else:
            if string_char in mapped_letters:
                return False
            mapping[ref_char] = string_char
            mapped_letters.add(string_char)

    return True


def match_ref_shape(string: str):
    # Length of string must match
    if len(string) != len(reference_str):
        return False

    spaces = set()
    letters = set()

    # Positions of spaces must match
    for c_ix, c in enumerate(string):
        if c == ' ':
            spaces.add(c_ix)
        else:
            letters.add(c)

    if spaces != space_pos:
        return False

    return True


def read_input():

    """ Read in all lines """
    lines = []
    for l in range(100):
        try:
            line = input().strip()
        except EOFError:
            break
        if line == "" or line == "\n":
            break

        lines.append(line)  # Save for decryption

    return lines


def build_mapping(line: str):
    mapping = {' ': ' '}

    for c_ix, c in enumerate(line):
        if c != ' ':
            mapping[c] = reference_str[c_ix]

    return mapping


def check_duplicates(line: str):
    for c_ix, c in enumerate(line):
        dup_pos = duplicates_by_pos.get(c_ix, [])
        for dup_ix in dup_pos:
            if line[c_ix] != line[dup_ix]:
                return False

    return True


def apply_mapping(line: str, mapping: dict):
    decryption = ['x'] * len(line)
    for c_ix, c in enumerate(line):
        decryption[c_ix] = mapping[c]

    return "".join(decryption)


if __name__ == '__main__':

    n_cases = int(input())
    input()  # Skip empty first line
    for testcase in range(n_cases):
        lines = read_input()

        ref_match_found = -1

        # Search every line for the permutated reference string
        for l, line in enumerate(lines):
            if len(reference_str) != len(line):
                # print("Length doesn't match")
                continue
            if not match_ref_shape(line):
                # print("Shape does not match reference")
                continue
            if not is_bijective_mapping(line):
                # print("No bijective mapping")
                continue
            if not check_duplicates(line):
                # print("Duplicate at wrong position")
                continue

            ref_match_found = l
            break

        if ref_match_found == -1:
            print("No solution.\n")
            continue

        # Build mapping
        mapping = build_mapping(lines[ref_match_found])

        # cache solutions, if there is an error here print no solution else print solutions
        for line in lines:
            decryption = apply_mapping(line, mapping)
            print(decryption)

        print("")

