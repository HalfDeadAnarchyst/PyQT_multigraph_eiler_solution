from graphlib import *
from heli import *
import csv
from tqdm import tqdm


def calc_money(distance, heli, k_vp):
    c_vp = (heli.mass_full / 1000) * 9500 * heli.koef_diff
    cost_aeno = (heli.cost_aeno * 1000 * heli.fuel * 2) * 10 ** (-2)
    c_to = 5.2 * heli.cost_service * (heli.mass_empty / 1000) ** 0.845
    c_zp = 7.45 * heli.cost_crew * (heli.mass_empty / 1000) ** 0.069
    c_gsm = (float(heli.fuel_consum) / float(heli.time_engine)) * float(heli.cost_fuel) * float(heli.koef_gsm)
    c_per = 1.1 * (c_to + c_zp + c_gsm)
    c_ker = 5.85 * heli.cost_crew * (heli.mass_empty / 1000) ** 0.83
    c_lch = c_per + c_ker
    hours = distance / heli.curce_speed
    cost_all = c_lch * hours + (c_vp + cost_aeno) * k_vp
    return cost_all


def get_path_cost(v_base, path, distance, heli):
    k_vp = 0
    for v_cur in path:
        if v_cur == v_base:
            k_vp = k_vp + 1
    return calc_money(distance, heli, k_vp)


def find_longest_path(v_cur, v_base, path, result, traveled_distance, max_fuel, cur_fuel, i, heli, k):

    '''
    try:
        distance = 0
        for p in range(0, len(result)-1):
            distance += result[p].conns[result[p + 1]]
        if distance != traveled_distance:
            print(result)
            print(distance)
            print(traveled_distance)

            print("\n")
    except Exception as e:
        print(e)
    '''

    i = i + 1
    # full_flight, no fuel, no flight
    if v_cur == v_base:
        cur_fuel = max_fuel
        traveled_distance += 0  # cost of refuel

    temp_paths = []
    for road in path:
        if road[0] == v_cur:  # This is where we are now
            if road not in temp_paths:
                temp_paths.append(road)

    temp_res = []
    if temp_paths:
        for road in temp_paths:
            if (cur_fuel - road[2]) >= road[1].conns[v_base]:  # if enough fuel to fly home after next point
                path_backup = path.copy()  # path copy
                res_backup = result.copy()  # result_copy
                res_backup.append(path_backup.pop(path_backup.index(road))[1])
                temp_distance = traveled_distance + v_cur.conns[road[1]]
                temp_res.append(find_longest_path(
                    road[1], v_base,
                    path_backup.copy(), res_backup.copy(),
                    temp_distance,
                    max_fuel, cur_fuel - road[2],
                    i,
                    heli,
                    k))
            else:
                return i, result, traveled_distance, path
    else:
        return i, result, traveled_distance, path

    if len(temp_res) > 1:
        for _ in range(0, len(temp_res) - 1):
            if temp_res[0][0] > temp_res[1][0]:
                temp_res.remove(temp_res[1])
            elif temp_res[0][0] < temp_res[1][0]:
                temp_res.remove(temp_res[0])
            else:  # money here
                if get_path_cost(v_base, path, temp_res[0][2], heli) > get_path_cost(v_base, path, temp_res[1][2], heli):
                    temp_res.remove(temp_res[0])
                else:
                    temp_res.remove(temp_res[1])
    elif len(temp_res) == 0:
        return i, result, traveled_distance, path

    temp_res = temp_res[0]
    return temp_res[0], temp_res[1], temp_res[2], temp_res[3]


def find_best_path(v_cur, v_base, path, result, traveled_distance, max_fuel, cur_fuel, i, heli, k):

    i = i + 1
    # full_flight, no fuel, no flight
    temp_res = []
    if v_cur == v_base:
        cur_fuel = max_fuel
        # traveled_distance += 0  # cost of refuel

    if not path:  # no more flights left
        # print(result, spent_money)
        return result, traveled_distance

    temp_paths = []
    for road in path:
        if road[0] == v_cur:  # This is where we are now
            if road not in temp_paths:
                temp_paths.append(road)

    v_left = []
    for road in path:
        if not road[0] in v_left:
            v_left.append(road[0])

    if temp_paths:
        for road in temp_paths:
            if (cur_fuel - road[2]) >= road[1].conns[v_base] * k:  # if enough fuel to fly home after next point
                path_backup = path.copy()  # path copy
                res_backup = result.copy()  # result_copy
                res_backup.append(path_backup.pop(path_backup.index(road))[1])
                temp_distance = traveled_distance + v_cur.conns[road[1]]
                # traveled_distance += v_cur.conns[road[1]]
                temp_res.append(find_best_path(
                    road[1], v_base,
                    path_backup.copy(), res_backup.copy(),
                    temp_distance,
                    max_fuel, cur_fuel - road[2],
                    i,
                    heli,
                    k))
            else:
                # traveled_distance += v_cur.conns[v_base] * k  # fly to base to refuel
                temp_distance = traveled_distance + v_cur.conns[v_base] * k
                res_backup = result.copy()  # result_copy
                res_backup.append(v_base)
                temp_res.append(find_best_path(
                    v_base, v_base,
                    path.copy(), res_backup,
                    temp_distance,
                    max_fuel, cur_fuel,
                    i,
                    heli,
                    k))

    else:  # no task in current vertice
        v_next = v_left[0]
        for v_var in v_left:  # FOR CLOSEST
            if v_cur.conns[v_var] > v_cur.conns[v_next]:
                v_next = v_var

        if (cur_fuel - v_cur.conns[v_next]) * k >= v_cur.conns[v_base] * k:  # if enough fuel to fly home after next point
            # traveled_distance += v_cur.conns[v_next] * k
            temp_distance = traveled_distance + v_cur.conns[v_next] * k
            cur_fuel = cur_fuel - v_cur.conns[v_next]
            res_backup = result.copy()
            res_backup.append(v_next)
            temp_res.append(find_best_path(
                v_next, v_base,
                path.copy(), res_backup,
                temp_distance,
                max_fuel, cur_fuel,
                i,
                heli,
                k))
        else:
            # traveled_distance += v_cur.conns[v_base] * k
            temp_distance = traveled_distance + v_cur.conns[v_base] * k
            res_backup = result.copy()
            res_backup.append(v_base)
            temp_res.append(find_best_path(
                v_base, v_base,
                path.copy(), res_backup,
                temp_distance,
                max_fuel, cur_fuel,
                i,
                heli,
                k))

    # print(temp_res) # and money here
    while type(temp_res) is not tuple:
        for _ in range(0, len(temp_res) - 2):
            # get_path_cost(v_base, path, temp_res[0][1], heli)
            if get_path_cost(v_base, path, temp_res[0][1], heli) < get_path_cost(v_base, path, temp_res[1][1], heli):
                temp_res.remove(temp_res[1])
            else:
                temp_res.remove(temp_res[0])
        temp_res = temp_res[0]
    return temp_res[0], temp_res[1]


# import cities list from csv, a is line, i is number
def load_data():
    data = list(csv.reader(open('cities.csv', encoding='utf-8')))
    cities = [Vertex(a[0], a[1], a[2], f"city_{i + 1}") for i, a in enumerate(data[1:])]
    return cities


def load_helicopter():
    heli = Helicopter("Mi-8P", 1, 550.0, 1, 225.0, 7000.0, 11570.0, 1470.0, 3.0,
                      1.04, 1.0, 300.0, 100.0, 27.0, 214.0, 550.0)
    return heli


def prepare_graph(cities_db):
    # add all cities to graph class
    g = Graph()
    for city in cities_db:
        g.vertices.append(city)
    g.calc_distances()
    return g


def graph_gen_tasks(g, helicopter):
    g.generate_tasks()  # or import tasks here
    g.make_edges(helicopter.seats)

#  for v1 in g.vertices:
#      print(v1.edges)

#  for conn in g.connections:
#      print(conn)


def prepare_paths(g):
    # gather all paths for first run
    paths = []
    for v1 in g.vertices:
        for edge in v1.edges:
            if edge[3]:
                paths.append(edge)
    return paths

# print(len(paths), paths)


def find_non_full_run(paths, heli, g):
    results = []
    for v1 in tqdm(g.vertices):
        copy_paths = paths.copy()
        # results.append([v1, find_best_path(v1, v1, copy_paths, [v1], 0, heli.fuel, heli.fuel, 0)])
        k = 1
        results.append([v1, find_longest_path(v1, v1, copy_paths, [v1], 0, heli.fuel, heli.fuel, 0, heli, k)])
    return results


def find_rest_full_run(results, heli):
    output = []
    for res in results:
        # print("\n", res)
        res[1][1].append(res[0])  # return to base, don't FORGET TO ADD FUEL TO FLY HOME
        k = 1
        res = find_best_path(res[0], res[0], res[1][3].copy(), res[1][1], res[1][2], heli.fuel, heli.fuel, res[1][0],
                             heli, k)
        # print(len(res[0]), res)
        output.append(res)
    return output


def get_best_result(results):
    best_result = []
    for res in results:
        if len(best_result) == 0:
            best_result = res
        else:
            if best_result[1] > res[1]:
                best_result = res
    return best_result
# print("\n", best_result)


def test_launch():
    city_db = load_data()
    heli_db = load_helicopter()
    g = prepare_graph(city_db)
    graph_gen_tasks(g, heli_db)
    paths_list = prepare_paths(g)
    non_full_run_list = find_non_full_run(paths_list, heli_db, g)
    best_runs_list = find_rest_full_run(non_full_run_list, heli_db)
    best_run = get_best_result(best_runs_list)
    print(best_run)


# test_launch()
# city_db = load_data()
# heli_db = load_helicopter()
# g = prepare_graph(city_db)
# g.generate_tasks()
# print(g.tasks)
