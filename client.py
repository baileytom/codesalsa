#!/usr/bin/python

import sys
import json
import random

from implementation import *


if (sys.version_info > (3, 0)):
    print("Python 3.X detected")
    import socketserver as ss
else:
    print("Python 2.X detected")
    import SocketServer as ss


class NetworkHandler(ss.StreamRequestHandler):
    def handle(self):
        game = Game()

        while True:
            data = self.rfile.readline().decode() # reads until '\n' encountered
            json_data = json.loads(str(data))
            # uncomment the following line to see pretty-printed data
            # print(json.dumps(json_data, indent=4, sort_keys=True))
            #response = game.get_random_move(json_data).encode()
            response = game.get_moves(json_data).encode()
            self.wfile.write(response)



class Game:
    def __init__(self):
        self.units = set() # set of unique unit ids
        self.directions = ['N', 'S', 'E', 'W']
        self.map = Map()
        #self.map.show_map()

        # Game stages
        # Stage 1: Gather & search
        #   - Mass produce scouts
        #   - Scouts in search mode, target unknown space
        # Stage 2: (Found base) Attack
        #   - All units attack

        #for

        self.stage = 1

    def get_random_move(self, json_data):
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter
        unit = random.choice(tuple(self.units))
        direction = random.choice(self.directions)
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit, "dir": direction}]}
        response = json.dumps(command, separators=(',',':')) + '\n'
        return response

    def respond(self, json_data):
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units  # add any additional ids we encounter
        #for unit in units:
        #for unit in units:
        #    if self._units[unit['id']] == None:

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal):

        graph = SquareGrid(self.map)

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        print(current, next)

        return

        #return came_from, cost_so_far

    def get_moves(self, json_data):
        unit_updates = json_data['unit_updates']
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units

        #print(json_data['tile_updates'])

        for tile in json_data['tile_updates']:
            if not tile['visible']:
                self.map.invisible.append((tile['x'], tile['y']))
                continue
            else:
                try:
                    self.map.invisible.remove((tile['x'], tile['y']))
                except:
                    pass

            #print(str(tile) + "\n")
            # Tile
            # x, y, visible, blocked, resources : {id, type, total, value?}
            if tile['blocked']:
                    self.map.settile(tile['x'], tile['y'], 1)
                    self.map.walls.append((tile['x'], tile['y']))
            try:
                #print(tile['resources'])
                if tile['resources'] != None:
                    self.map.settile(tile['x'], tile['y'], "r")
                    self.map.resources.append((tile['x'], tile['y']))
            except:
                pass



        for unit in unit_updates:
            move = None
            location = (unit['x'], unit['y'])
            unit['target'] = location
            if self.stage == 1:
                if unit['type'] == 'worker':
                    try:
                        unit['target'] = self.map.resources[0]
                    except:
                        pass
                    try:
                        unit['target'] = self.map.invisible[0]
                    except:
                        pass

                    move = self.a_star_search(location, unit['target'])
                    # Do worker stuff
                elif unit['type'] == 'scout':
                    pass
                    # Do scout stuff
            elif self.stage == 2:
                if unit['type'] == 'worker':
                    pass
                    # Do worker stuff
                elif unit['type'] == 'scout':
                    pass
                    # Scout

        self.map.show_map()

        unit = random.choice(tuple(self.units))
        direction = random.choice(self.directions)
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit, "dir": direction}]}
        response = json.dumps(command, separators=(',', ':')) + '\n'
        return response



class Map:
    def __init__(self):
        self.grid = [[0 for y in range(0,60)] for x in range(0, 60)]
        self.originx = 29
        self.originy = 29
        self.grid[self.originx][self.originy] = 1

        self.resources = []
        self.walls = []
        self.invisible = []

    def show_map(self):
        print(self.resources)
        for x in self.grid:
            print_str = ""
            for y in x:
                print_str += ("{} ".format(y))
            print(print_str)

    def settile(self, x, y, value):
        self.grid[x+self.originx][y+self.originy] = value

    def gettile(self, x, y):
        return self.grid[x+self.originx][y+self.originy]
"""

class Unit:
    def __init__(self):
        self.x, self.y = 0, 0;

class Worker(Unit):
    def __init__(self):
        super.__init__(self)

    def get_move(self, game):

class Tank(Unit):
    def __init__(self):
        super.__init__(self)
        #self.hp =
    #def

"""
if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '10.8.2.42'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
