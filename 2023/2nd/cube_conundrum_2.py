import re

with open("./2nd/cube_conundrum_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

sum_result = 0

def get_amount_from_poll(color, poll):
    return int(re.sub(f' {color}', '', (re.search(fr'\d+ {color}', poll) or re.search('0', '0')).group()))

for game in lines:

    game_id = int(re.sub("Game ", '', re.search(r"Game \d+", game).group()))
    polls = re.split(';', re.split(':', game)[-1])

    max_reds = 0
    max_greens = 0
    max_blues = 0

    for poll in polls:

        reds = get_amount_from_poll('red', poll)
        greens = get_amount_from_poll('green', poll)
        blues = get_amount_from_poll('blue', poll)

        if reds > max_reds:
            max_reds = reds

        if greens > max_greens:
            max_greens = greens
        
        if blues > max_blues:
            max_blues = blues
    
    product = max_reds * max_greens * max_blues
    sum_result += product
    

print(sum_result)