import csv, pandas


def split_by_street():
    city_map = pandas.read_csv(
        "map.csv", sep=";", engine="python", skiprows=1, header=None
    )
    counter = 0
    city = {}
    for i in city_map.iterrows():
        city[counter] = i
        counter += 1
    return city


map_by_streets = split_by_street()


def house_filter(house):
    if (
        house[0] == "kertes ház"
        and house[1] == "piros"
        and house[2] == "magas kerítés"
        and house[3] == "2 emeletes"
    ):
        return True
    else:
        return False


def denoise(noisy_map):
    noiseless_map = []
    count_1 = 0
    for street in noisy_map:
        noiseless_map.append([])
        for house in noisy_map[street][1]:
            if type(house) is str:
                house = house.split(",")
                house = (house_filter(house), house[4])
                noiseless_map[count_1].append(house)
        count_1 += 1
    return noiseless_map


noiseless = denoise(map_by_streets)


def show_hideouts(city_map):
    hideouts = []
    street_counter = 0
    for street in city_map:
        house_counter = 0
        for house in street:
            if house[0]:
                hideouts.append((street_counter, house_counter))
            house_counter += 1
        street_counter += 1
    return hideouts


hideouts = show_hideouts(noiseless)


def get_edges(city_map):
    edges = []
    current_street = 0
    while current_street < len(city_map):
        current_house = 0
        while current_house < len(city_map[current_street]):
            if current_house == 0 or current_house == len(city_map[0]) - 1:
                if current_street != len(city_map) - 1:
                    edges.append(
                        (
                            str(current_street) + "-" + str(current_house),
                            str(current_street + 1) + "-" + str(current_house),
                            int(city_map[current_street][current_house][1]),
                        )
                    )
            if current_house != len(city_map[0]) - 1:
                edges.append(
                    (
                        str(current_street) + "-" + str(current_house),
                        str(current_street) + "-" + str(current_house + 1),
                        int(city_map[current_street][current_house][1]),
                    )
                )
            current_house += 1
        current_street += 1
    return edges


edges = get_edges(noiseless)
