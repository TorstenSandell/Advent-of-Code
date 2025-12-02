import re

with open("./4th/scratchcards_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

total_cards = 0
card_instances = {card_number : 1 for card_number in range(1, len(lines) + 1)}

for card in lines:
    card_number = int(re.sub(r':.+', '',re.sub(r'Card\s+', '', card)))
    card_info = re.sub(r'Card\s+\d+:\s+', '', card)

    card_amount = card_instances[card_number]

    numbers = card_info.split(' | ')
    game_numbers = list(filter(None, numbers[0].split(' ')))
    goal_numbers = list(filter(None, numbers[1].split(' ')))

    wins = 0
    for number in game_numbers:
        if number in goal_numbers:
            wins += 1
    for card in range(card_number + 1, card_number + wins + 1):
        if card <= len(card_instances):
            card_instances[card] += card_amount

print(sum(list(card_instances.values())))
