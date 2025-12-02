with open("./1st/trebuchet_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

result = []
numbers = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
           "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9}

def check_for_number(i, line):
    for number in numbers.keys():
        index_end_of_number_in_line = i + len(number)
        if index_end_of_number_in_line <= len(line):
            if line[i:(index_end_of_number_in_line)] == number:
                return numbers[number]
    return None

for line in lines:
    first = ''
    last = ''
    for i in range(len(line)):
        number = check_for_number(i, line)
        if number:
            first = number
            break
    for i in reversed(range(len(line))):
        number = check_for_number(i, line)
        if number:
            last = number
            break
    result += [int(f'{first}{last}')]

print(sum(result))
