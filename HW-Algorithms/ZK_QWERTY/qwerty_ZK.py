def add_prefix(p: str, words: list[str]) -> list[str]:
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
    def __init__(self, name: str | None,
                 phone: int | None = None,
                 is_root: bool = False):
        self.is_root = is_root
        self.children = []
        self.children_letters = []
        self.name = name
        self.phone = phone

    def add_name(self, name: str, phone: int):
        # TODO: Wenn neues Child, einmal durchiterieren, um Position (alphabetisch) zu finden, dort einfügen
        print(f"Add string: {name}, phone: {phone}")
        if name[0] != '$':
            for child_ix, child_letter in enumerate(self.children_letters):
                if child_letter == name[0]:
                    print(f"Found letter {name[0]} in child {child_ix}, add {name[1:]} there")
                    self.children[child_ix].add_name(name[1:], phone)
                    return
            print("Letter not found, create new child")
            self.children.append(NameTreeNode(name=name[0]))
            self.children_letters.append(name[0])
            self.children[len(self.children) - 1].add_name(name[1:], phone)

        else:  # Assumes names are not doubled
            print("Last node reached, add $ node")
            self.children.append(NameTreeNode("$", phone))
            self.children_letters.append("$")

    def search_name(self, name: str) -> [bool, int]:

        for child_ix, child_letter in enumerate(self.children_letters):
            if child_letter == name[0]:
                print(f"Found letter {name[0]} in child {child_ix}")
                if name[1:] == '$':
                    print(f"Yes, match found. Now count own suffixes in {self.children_letters}: {self.get_n_suffixes(True)}")
                    return True, self.children[child_ix].get_n_suffixes(True)
                return self.children[child_ix].search_name(name[1:])

        # n_suffixes = 0
        # for child in self.children:
            # n_suffixes += child.get_n_suffixes()

        return [False, 42]

    def get_n_suffixes(self, last_match: bool) -> int:
        n_suffixes = 0
        print(self.children_letters)
        for child in self.children:
            if not (child.name == "$" and last_match):
                n_suffixes += child.get_n_suffixes(False)
        print(n_suffixes, self.name)
        print(len(self.children))
        if self.is_leaf():
            return 1

        return n_suffixes

    def filter_query(self, query: str):
        poss = []
        next_letters = key_map.get(query[0])

        for l in next_letters:
            for i, x in enumerate(self.children_letters):
                if x == l and len(query) > 1:
                    poss.append( *add_prefix(l, self.children[i].filter_query(query[1:])) )
                    break
                elif x == l:
                    poss.append(l + str(self.children[i].phone))

        return poss

    def print_vals(self):
        for child in self.children:
            child.print_vals()

        print(self.name)

    def is_leaf(self):
        return len(self.children) == 0


if __name__ == '__main__':
    key_map = {
        '1': ['q', 'w', 'e'],
        '2': ['r', 't', 'y', 'u'],
        '3': ['i', 'o', 'p'],
        '4': ['a', 's', 'd'],
        '5': ['f', 'g', 'h'],
        '6': ['j', 'k', 'l'],
        '7': ['z', 'x', 'c'],
        '8': [' '],
        '9': ['v', 'b', 'n', 'm']
    }

for case in range(int(input())):
    phone_book = NameTree()
    n_entries = int(input())

    for entry in range(n_entries):
        nom, phone_str = input().split(" ")
        phone_book.add_name(nom, phone_str)

    print(phone_book.filter_query("9393"))
    # print(phone_book.search_name("mo"))
    # phone_book.print_vals()
    # n_queries = int(input())
    # for query in range(n_queries):

