
if __name__ == '__main__':
    value_range = [x for x in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
    value_ics = {2: 0, 3: 1, ..., 'A': ...}

    for t in range(int(input())):
        card_deck = {'C': value_range.copy(), 'D': value_range.copy(), 'H': value_range.copy(), 'S': value_range.copy()}
        n = int(input())
        for i in range(n):
            val, suit = input().split(' ')
            card_deck[suit][val] = i