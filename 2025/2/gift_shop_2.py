debug = False

with open("./2025/2nd/input.txt", mode="r") as input:
    lines = input.read().split(',')

ranges = [tuple(line.split('-')) for line in lines]

def pr(value):
    if debug:
        print("  " + str(value))
    return value

sum_invalid = 0
for start, stop in ranges:
    for value in range(int(start), int(stop)+1):
        value = str(value)
        n_digits = len(value)
        max_check = int(n_digits / 2)
        for slice_size in range(1, max_check + 1):
            if int(n_digits / slice_size) * slice_size != n_digits:
                continue
            n_segments = int(n_digits / slice_size)

            val = None
            invalid = True
            for i in range(n_segments):
                slice_start = i * slice_size
                slice_end = slice_start + slice_size
                slice_val = value[slice_start:slice_end]
                if val is None:
                    val = slice_val
                elif val != slice_val:
                    invalid = False
                    break

            if invalid:
                sum_invalid += int(value)
                break


print(sum_invalid)