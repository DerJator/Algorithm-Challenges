def add_prefix(p: str, words: list):  # str, list[str] -> list[str]
    return [p + el for el in words]


class NameTree:
    def __init__(self):
        self.root = NameTreeNode(name=None, phone=None, is_root=True)

    def add_name(self, name: str, phone: str):
        self.root.add_name(name + '$', int(phone))

    def search_name(self, name: str) -> [bool, int]:
        match_found, n_prefixes = self.root.search_name(name + '$')

        return [match_found, n_prefixes]

    def filter_query(self, query: str) -> [str]:
        return self.root.filter_query(query)

    def print_vals(self):
        self.root.print_vals()


class NameTreeNode:
    def __init__(self, name: str,  # str|None
                 phone: int = None,  # int|None
                 is_root: bool = False):  # bool
        self.is_root = is_root
        self.children = []
        self.children_letters = {}
        self.name = name
        self.phone = phone

    def add_name(self, name: str, phone: int):
        # TODO: Wenn neues Child, einmal durchiterieren, um Position (alphabetisch) zu finden, dort einfügen
        # print(f"Add string: {name}, phone: {phone}")
        if name[0] != '$':
            next_child = self.children_letters.get(name[0])
            if next_child is not None:
                # print(f"Found letter {name[0]} in a child, add {name[1:]} there")
                next_child.add_name(name[1:], phone)
                return
            # print("Letter not found, create new child")
            # self.children.append(NameTreeNode(name=name[0]))
            new_child = NameTreeNode(name=name[0])
            self.children_letters[name[0]] = new_child
            new_child.add_name(name[1:], phone)

        else:  # Assumes names are not doubled
            # print("Last node reached, add $ node")
            self.children_letters["$"] = NameTreeNode("$", phone)
            # self.children_letters.append("$")

    def search_name(self, name: str) -> [bool, int]:

        child = self.children_letters.get(name[0])
        if child is not None:
            # print(f"Found letter {name[0]} in child")
            if name[1:] == '$':
                # print(f"Yes, from {self.name} match found. Now count own suffixes in {self.children_letters.keys()}: ")
                return True, child.get_n_suffixes(True)
            return child.search_name(name[1:])

        # n_suffixes = 0
        # for child in self.children:
            # n_suffixes += child.get_n_suffixes()

        return [False, 42]

    def get_n_suffixes(self, last_match: bool) -> int:
        n_suffixes = 0
        # print(f"I'm {self.name}, {last_match=}, children: {self.children_letters}")
        for c_letter, child in self.children_letters.items():
            if not (c_letter == "$" and last_match):
                # print(f"get suffixes from {c_letter}")
                n_suffixes += child.get_n_suffixes(False)
        # print(n_suffixes, self.name)
        # print(len(self.children_letters))
        if self.is_leaf():
            # print(f"I, {self.name}: return 1")
            return 1

        return n_suffixes

    def filter_query(self, query: str):
        poss = []
        next_letters = key_map.get(query[0])

        for l in next_letters:  # [O(3-4)]
            child = self.children_letters.get(l)
            if child is not None:
                if len(query) > 1:
                    poss.append( *add_prefix(l, child.filter_query(query[1:])) )  # Get word through tree [O(log
                else:
                    leaf_child = child.children_letters.get("$")
                    if leaf_child is not None:
                        poss.append(l + " " + str(child.children_letters.get("$").phone))
                    else:
                        poss.append(l + " X")

        return poss

    def print_vals(self):
        for child in self.children_letters.values():
            child.print_vals()

        # print(self.name, self.phone)

    def is_leaf(self):
        return len(self.children_letters.items()) == 0


if __name__ == '__main__':
    # Important: Sorted alphabetically per key, determines search order
    key_map = {
        '1': ['e', 'q', 'w'],
        '2': ['r', 't', 'u', 'y'],
        '3': ['i', 'o', 'p'],
        '4': ['a', 'd', 's'],
        '5': ['f', 'g', 'h'],
        '6': ['j', 'k', 'l'],
        '7': ['c', 'x', 'z'],
        '8': [' '],
        '9': ['b', 'm', 'n', 'v']
    }

for case in range(int(input())):
    phone_book = NameTree()
    n_entries = int(input())

    # Build phone book [O(n)]
    for entry in range(n_entries):
        nom, phone_str = input().split(" ")
        phone_book.add_name(nom, phone_str)

    n_queries = int(input())
    for j in range(n_queries):
        n_suffix = 0
        q = input()
        matches = phone_book.filter_query(q)
        no_match_flag = True
        for match in matches:
            name, phone = match.split(" ")
            n_suffix += phone_book.search_name(name)[1]  # This one could be too inefficient,
        # traversal for every name separately
            if phone != "X":
                print(match)
                no_match_flag = False

        if no_match_flag:
            print("no entries found")
        print(n_suffix)
    print()

