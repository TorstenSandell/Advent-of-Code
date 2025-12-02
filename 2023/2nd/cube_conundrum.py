import re

with open("./2nd/cube_conundrum_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

max_reds = 12
max_greens = 13
max_blues = 14
sum_result = 0

def get_amount_from_poll(color, poll):
    return int(re.sub(f' {color}', '', (re.search(fr'\d+ {color}', poll) or re.search('0', '0')).group()))

for game in lines:
    impossible = False

    game_id = int(re.sub("Game ", '', re.search(r"Game \d+", game).group()))
    polls = re.split(';', re.split(':', game)[-1])

    for poll in polls:

        reds = get_amount_from_poll('red', poll)
        greens = get_amount_from_poll('green', poll)
        blues = get_amount_from_poll('blue', poll)

        if reds > max_reds or greens > max_greens or blues > max_blues:
            impossible = True
            break
    
    if not impossible:
        sum_result += game_id

print(sum_result)