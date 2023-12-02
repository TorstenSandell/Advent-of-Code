with open("./1st/trebuchet_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

result = []

for line in lines:
    first = ''
    last = ''
    for i in range(len(line)):
        if (line[i].isdigit()):
            first = line[i]
            break
    for i in reversed(range(len(line))):
        if (line[i].isdigit()):
            last = line[i]
            break
    
    result += [int(f'{first}{last}')]

print(sum(result))
