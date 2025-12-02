import re
from math import sqrt, floor, ceil
from collections import Counter

with open("./7th/camel_cards_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

hands = {
    'five': [],
    'four': [],
    'full': [],
    'three': [],
    '2_pair': [],
    'pair': [],
    'high': []
}

for line in lines:
    hand, bid = line.split(' ')
    cnt = Counter(list(hand))
    entry = [(hand, int(bid))]
    fours = 0
    triples = 0
    pairs = 0
    jokers = cnt['J']
    easily_found = False
    for key, value in cnt.items():
        if key == 'J':
            continue

        if value == 5:
            hands['five'] += entry
            easily_found = True
            break
        elif value == 4:
            fours += 1
        elif value == 3:
            triples += 1
        elif value == 2:
            pairs += 1
    
    if not easily_found:
        if jokers == 0:
            if fours == 1:
                hands['four'] += entry
            elif triples == 1 and pairs == 1:
                hands['full'] += entry
            elif triples == 1:
                hands['three'] += entry
            elif pairs == 2:
                hands['2_pair'] += entry
            elif pairs == 1:
                hands['pair'] += entry
            else:
                hands['high'] += entry
        else:
            if fours == 1 and jokers == 1 or \
                triples == 1 and jokers == 2 or \
                pairs == 1 and jokers == 3 or \
                jokers == 4 or jokers == 5:
                hands['five'] += entry
            elif triples == 1 and jokers == 1 or \
                pairs == 1 and jokers == 2 or \
                pairs == 0 and jokers == 3:
                hands['four'] += entry
            elif pairs == 2 and jokers == 1:
                hands['full'] += entry
            elif pairs == 1 and jokers == 1 or \
                pairs == 0 and triples == 0 and jokers == 2:
                hands['three'] += entry
            elif pairs == 0 and triples == 0 and fours == 0 and jokers == 1:
                hands['pair'] += entry
            

def get_card_worth(card):
    if card == 'A':
        return 14
    if card == 'K':
        return 13
    if card == 'Q':
        return 12
    if card == 'J':
        return 1
    if card == 'T':
        return 10
    return int(card)

def assign_points(hand):
    """
    A ten digit number where every pair of number represents the value of a card
    """
    hand = list(hand)
    points = 0
    for i, card in enumerate(hand):
        points += get_card_worth(card) * 10**(2*(5-i))
    return points

for hand_rank, entries in hands.items():
    hands[hand_rank] = sorted(entries, key=lambda x: assign_points(x[0]), reverse=True)

all_hands_sorted = hands['five']+hands['four']+hands['full']+hands['three']+hands['2_pair']+hands['pair']+hands['high']

result = 0
max_rank = len(all_hands_sorted)

for i, hand in enumerate(all_hands_sorted):
    bid = hand[1]
    result += bid * (max_rank-i)

print(result)