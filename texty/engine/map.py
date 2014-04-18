from texty.builtins.room import Room
import csv
import re

class Map(object):
    """
    Map
    """
    def __init__(self):
        self.rooms = {}

    def load_data(self, map_file, room_file):
        """
        Read map data from a CSV file.
        """
        map_reader = csv.reader(open(map_file, 'U'))
        room_reader = csv.reader(open(room_file, 'U'))

        # store reference arrays to the last north and up cells
        n = [None]
        u = [None]

        for row in map_reader:
            # store reference to the last west cell
            w = None

            for x, room in enumerate(row):
                # expand north and up lists if required
                if len(n) <= x: n.append(None)
                if len(u) <= x: u.append(None)

                # test what kind of cell we are dealing with
                if re.match(r'[A-Z]\d+', room):
                    # this is a room
                    # create it if it doesn't yet exist
                    if not self.rooms.has_key(room):
                        self.rooms[room] = Room(room)
                    # check for exits
                    if w:
                        # west reference is set, so make exits
                        self.rooms[room].exits['west'] = w
                        w.exits['east'] = self.rooms[room]
                    if u[x]:
                        # up reference is set, so make exits
                        self.rooms[room].exits['up'] = u[x]
                        u[x].exits['down'] = self.rooms[room]
                    elif n[x]:
                        # north reference is set, so make exits
                        self.rooms[room].exits['north'] = n[x]
                        n[x].exits['south'] = self.rooms[room]
                    # set north and west references
                    w = n[x] = u[x] = self.rooms[room]

                elif room == '.':
                    # this is a horizontal link, so clear the up reference
                    u[x] = None
                elif room == '%':
                    # TODO: one way, or door, needs logic here
                    u[x] = None
                elif room == '|':
                    # this is a vertical link, so clear the north and west references
                    n[x] = w = None
                else:
                    # this is a blank cell, so clear all references
                    w = n[x] = u[x] = None

        for row in room_reader:
            # loop through room list, and attach titles and descriptions
            if len(row) == 0: continue
            room = row[0]
            if not self.rooms.has_key(room): continue
            if len(row) == 1: continue
            self.rooms[room].title = row[1]
            if len(row) == 2: continue
            self.rooms[room].description = row[2]

        # sweet, we have a map.