from texty.engine.room import Room, Edge
from texty.util.enums import DIRECTIONS as DIR
import collections
import csv
import itertools
import re

class Map(object):
    """
    A Map is a simple graph of connected rooms. There is not a large reason at the moment
    this could not be represeted by a simple dict instead.
    """

    def __init__(self):
        self.rooms = {}

    def load_excel(self, xlsx_filename, map_filename, rooms_filename):
        """
        Read map and room data from an Excel workbook and write them to csv files.
        Requires two sheets called "map" and "rooms"
        """
        import xlrd

        workbook = xlrd.open_workbook(xlsx_filename)

        def sheet_generator(sheet, out):
            """
            Generator to yield rows from an excel workbook sheet
            """
            writer = csv.writer(out)
            for row in range(sheet.nrows):
                cols = sheet.row_values(row)
                writer.writerow(cols)

        # load all sheets from the excel file,
        with open(map_filename, 'w') as m, open(rooms_filename, 'w') as r:
            for sheet in workbook.sheets():
                if 'room' in sheet.name.lower():
                    sheet_generator(sheet, r)
                else:
                    sheet_generator(sheet, m)


    def load_csv(self, map_filename, rooms_filename):
        """
        Read map data from a CSV file.
        """
        with open(map_filename, 'U') as m, open(rooms_filename, 'U') as r:
            self.load_map(csv.reader(m))
            self.load_rooms(csv.reader(r))


    def load_rooms(self, room_iterator):
        """
        Load the room data from an iterator.
        """
        for row in room_iterator:
            # loop through room list, and attach titles and descriptions
            if len(row) == 0:
                continue
            room = row[0]
            if not room in self.rooms:
                continue
            if len(row) == 1:
                continue
            self.rooms[room].name = row[1]
            if len(row) == 2:
                continue
            self.rooms[room].description = row[2]


    def load_map(self, map_iterator):
        """
        Load the map data from an iterator.
        """

        # store reference arrays to the last north and up cells
        north = []
        up = []

        for row in map_iterator:
            # store reference to the last west cell
            west = None

            for x, room_id in enumerate(row):

                # expand north and up lists if required
                if len(north) <= x:
                    north.append(None)

                if len(up) <= x:
                    up.append(None)

                # test what kind of cell we are dealing with
                if re.match(r'[A-Z]+\d+', room_id):

                    # this is a room
                    # create it if it doesn't yet exist
                    room = self.rooms.get(room_id, Room(room_id))
                    self.rooms[room_id] = room

                    # check for exit references
                    # west reference is set, so make exits
                    if west:
                        room.exits[DIR.WEST]        = west
                        west.exits[DIR.EAST]        = room

                    # north reference is set, so make exits
                    if north[x]:
                        room.exits[DIR.NORTH]       = north[x]
                        north[x].exits[DIR.SOUTH]   = room

                    # up reference is set, so make exits
                    elif up[x]:
                        room.exits[DIR.UP]          = up[x]
                        up[x].exits[DIR.DOWN]       = room

                    # set north, west and up references to this room
                    west        = room
                    north[x]    = room
                    up[x]       = room

                elif room_id == '.' or room_id == '..':
                    # this is a horizontal link, so clear the up reference
                    up[x]       = None

                elif room_id == '%':
                    # TODO: one way, or door, needs logic here
                    up[x]       = None

                elif room_id == '|':
                    # this is a vertical link, so clear the north and west references
                    north[x]    = None
                    west        = None

                else:
                    # this is a blank cell, so clear all references
                    west        = None
                    north[x]    = None
                    up[x]       = None

        # sweet, we have a map.
