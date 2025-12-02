import re

with open("./5th/if_you_give_seed_to_a_fertilizer_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

seeds = []
seed_values = re.sub("seeds: ", '', lines[0]).split(' ')
range_value = False
seed_start = 0

for value in seed_values:
    if not range_value:
        seed_start = int(value)

    else:
        range_value = int(value)
        seeds += [(seed_start, seed_start + range_value - 1)]

    range_value = not range_value

def get_map(map_name, lines):
    result = []
    found = False
    for line in lines:
        if found and line == '':
            break
        
        if found:
            destination, source, bound = [int(value) for value in line.split(" ")]
            result += [((source, source + bound - 1), destination - source, range(source, source + bound))]

        if re.match(fr"{map_name} map:", line):
            found = True
    return sorted(result, key=lambda x: x[0][0])

seed_to_soil = get_map('seed-to-soil', lines)
soil_to_fertilizer = get_map('soil-to-fertilizer', lines)
fertilizer_to_water = get_map('fertilizer-to-water', lines)
water_to_light = get_map('water-to-light', lines)
light_to_temperature = get_map('light-to-temperature', lines)
temperature_to_humidity = get_map('temperature-to-humidity', lines)
humidity_to_location = get_map('humidity-to-location', lines)

def index_with_range_in_map(index_range, map):
    lower_bound = index_range[0]
    upper_bound = index_range[1]
    new_ranges = []
    for mapping in map:
        mapping_lower_bound, mapping_upper_bound = mapping[0]
        
        mapping_range = mapping[2]
        mapping_mod = mapping[1]

        if lower_bound in mapping_range:
            if upper_bound in mapping_range:
                new_ranges += [(lower_bound + mapping_mod, upper_bound + mapping_mod)]
                break
            
            else:
                new_ranges += [(lower_bound + mapping_mod, mapping_upper_bound + mapping_mod)]
                lower_bound = mapping_upper_bound + 1

        elif lower_bound < mapping_lower_bound:
            if upper_bound < mapping_lower_bound:
                new_ranges += [(lower_bound, upper_bound)]
                break

            else:
                new_ranges += [(lower_bound, mapping_lower_bound - 1)]
                lower_bound = mapping_upper_bound + 1

    return new_ranges

def index_with_ranges_in_map(index_ranges, map):
    result = []
    for index_range in index_ranges:
        result += index_with_range_in_map(index_range, map)

    return sorted(result, key=lambda x: x[0])


soil = index_with_ranges_in_map(seeds, seed_to_soil)
fertilizer = index_with_ranges_in_map(soil, soil_to_fertilizer)
water = index_with_ranges_in_map(fertilizer, fertilizer_to_water)
light = index_with_ranges_in_map(water, water_to_light)
temperature = index_with_ranges_in_map(light, light_to_temperature)
humidity = index_with_ranges_in_map(temperature, temperature_to_humidity)
location = index_with_ranges_in_map(humidity, humidity_to_location)

best_location = sorted(location, key=lambda x: x[0])[0][0]

print(best_location)