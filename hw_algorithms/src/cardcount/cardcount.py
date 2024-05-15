if __name__ == '__main__':
    value_range = [str(x) for x in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
    value_range = value_range[::-1]
    suit_range = ['S', 'H', 'C', 'D']

    for t in range(int(input())):
        card_deck = {key: suit_range.copy() for key in value_range}
        n = int(input())
        for i in range(n):
            val, suit = input().split(' ')
            card_deck[val].remove(suit)
        for v, suits in card_deck.items():
            if len(suits) > 0:
                print(v, suits[0])
                break
