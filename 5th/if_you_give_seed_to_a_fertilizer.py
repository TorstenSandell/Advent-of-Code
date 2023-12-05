import re

with open("./5th/if_you_give_seed_to_a_fertilizer_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

seeds = re.sub("seeds: ", '', lines[0]).split(' ')

def get_map(map_name, lines):
    result = []
    found = False
    for line in lines:
        if found and line == '':
            break
        
        if found:
            destination, source, bound = [int(value) for value in line.split(" ")]
            result += [((source, source + bound - 1), destination - source)]

        if re.match(fr"{map_name} map:", line):
            found = True

    return result


seed_to_soil = get_map('seed-to-soil', lines)
soil_to_fertilizer = get_map('soil-to-fertilizer', lines)
fertilizer_to_water = get_map('fertilizer-to-water', lines)
water_to_light = get_map('water-to-light', lines)
light_to_temperature = get_map('light-to-temperature', lines)
temperature_to_humidity = get_map('temperature-to-humidity', lines)
humidity_to_location = get_map('humidity-to-location', lines)

def index_in_map(index, map):
    for entry in map:
        key = entry[0]
        if key[0] <= index and index <= key[1]:
            return entry[1] + index
    return index

best_location = -1

for seed in seeds:
    seed = int(seed)
    soil = index_in_map(seed, seed_to_soil)
    fertilizer = index_in_map(soil, soil_to_fertilizer)
    water = index_in_map(fertilizer, fertilizer_to_water)
    light = index_in_map(water, water_to_light)
    temperature = index_in_map(light, light_to_temperature)
    humidity = index_in_map(temperature, temperature_to_humidity)
    location = index_in_map(humidity, humidity_to_location)

    if best_location == -1 or location < best_location:
        best_location = location

print(best_location)