import math
import random


class Vertex:
    def __init__(self, name, lat, lon, the_id):
        self.name = name
        self.CanRefuel = False  # Can helicopter be refueled at this vertex
        self.conns = {}     # ConnDict template: {"Name", Distance in Km}, example:  {"Taganrog", 200}
        self.tasks = {}     # TaskDict template: {"Name", People Amount},  example:  {"Taganrog", 4}
        self.edges = []     # ["Name", Distance in Km, Is visited]
        self.lat = lat      # latitude
        self.lon = lon      # longitude
        self.the_id = the_id  # technical id

    def __repr__(self):
        return self.the_id


class Graph:
    def __init__(self):
        self.vertices = []     # [a, b, c], all should be Vertex class
        self.connections = []  # [[a, b, 200], [a, c, 300]]
        self.tasks = {}        # [[a, b, 4], [a, c, 9]]
        self.bases = []        # [a, c], where helicopter can be refueled

    def calc_distances(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 != v2:
                    distance = get_distance(float(v1.lat), float(v1.lon), float(v2.lat), float(v2.lon))
                    v1.conns[v2] = distance
                    v2.conns[v1] = distance
                    self.connections.append([v1, v2, distance])
                else:  # this is support for recursive algorithm find_all_paths
                    v1.conns[v1] = 0
                    self.connections.append([v1, v1, 0])

    def gather_tasks(self):
        self.tasks = {}
        self.tasks.clear()
        for v1 in self.vertices:
            self.tasks[v1] = v1.tasks

    def gather_bases(self):
        for v1 in self.vertices:
            if v1.CanRefuel:
                self.bases.append(v1)

    def generate_empty_tasks(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                v1.tasks[v2] = 0
        self.gather_tasks()

    def generate_tasks(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 != v2:
                    v1.tasks[v2] = abs(int(random.randint(0, 1)))
                else:
                    v1.tasks[v2] = 0
                    # v1.tasks[v2] = abs(int(random.normalvariate(0, 2)))
        self.gather_tasks()

    def delete_task(self, v1, v2):
        if type(v1) != Vertex or type(v2) != Vertex:
            print(f"Delete tasks input are not vertices, v1 is {type(v1)}, v2 is {type(v2)}")
        if self.tasks[v1][v2] != 0:
            v1.tasks[v2] = v1.tasks[v2] - 1
            self.gather_tasks()
        else:
            print(f"Got in delete task exception")
            print(f"tasks = {self.tasks}")
            print(f"tasks_v1 = {self.tasks[v1]}")
            print(f"tasks_v1_v2 = {self.tasks[v1][v2]}")

    def add_task(self, v1, v2):
        if v2 in v1.tasks:
            v1.tasks[v2] = v1.tasks[v2] + 1
        else:
            v1.tasks[v2] = 1
        self.gather_tasks()

    def make_edges(self, cargo_size):
        for v1 in self.vertices:
            for task in v1.tasks:
                for i in range(0, int((v1.tasks[task]) // cargo_size)):
                    #               verti | distance | is full cargo
                    v1.edges.append([v1, task, v1.conns[task], True])
                #               verti   distance      is full cargo      how many ppl left
                else:
                    if v1.tasks[task] % cargo_size != 0:
                        v1.edges.append([v1, task, v1.conns[task], False, v1.tasks[task] % cargo_size])


def get_distance(x1, y1, x2, y2):
    radius = 6373.0

    lat1 = math.radians(x1)
    lon1 = math.radians(y1)
    lat2 = math.radians(x2)
    lon2 = math.radians(y2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance
