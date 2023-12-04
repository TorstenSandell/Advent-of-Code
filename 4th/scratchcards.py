import re

with open("./4th/scratchcards_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

total_points = 0

for card in lines:
    card_info = re.sub(r'Card \s+\d+:\s+', '', card)
    numbers = card_info.split(' | ')
    game_numbers = list(filter(None, numbers[0].split(' ')))
    goal_numbers = list(filter(None, numbers[1].split(' ')))

    card_points = 0
    for number in game_numbers:
        if number in goal_numbers:
            if card_points == 0:
                card_points = 1
            else:
                card_points = card_points * 2
    
    total_points += card_points


print(total_points)