from collections import defaultdict

money = [200, 100, 50, 20, 10, 5, 2, 1]

if __name__ == '__main__':
    n_cases = int(input())

    for case in range(n_cases):
        inp = input()
        inp = int(inp.replace(".", ""))

        change = defaultdict(int)

        while inp > 0:
            for m in money:
                if inp - m >= 0:
                    inp -= m
                    change[m] = change[m] + 1
                    break

        print(f"Change for customer {case + 1}: ", end="")

        for m in money:
            print(f"{change[m]}x{m} ", end="")
        print("")