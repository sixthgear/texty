# from texty.engine.node import node
from texty.engine.node import Node, SENS
from texty.engine.parser import parser
from texty.util.enums import DIRECTIONS as DIR
import collections
import csv
import itertools
import re

class Map(object):
    """
    A Map is a simple graph of connected nodes.
    """

    def __init__(self):

        self.nodes = {}
        self.anonymous_nodes = []

    def load_excel(self, xlsx_filename, map_filename, nodes_filename):
        """
        Read map and node data from an Excel workbook and write them to csv files.
        Requires two sheets called "map" and "nodes"
        """
        import xlrd

        workbook = xlrd.open_workbook(xlsx_filename)

        def sheet_generator(sheet, out):
            """
            Generator to yield rows from an excel workbook sheet
            """
            writer = csv.writer(out, delimiter='\t')
            for row in range(sheet.nrows):
                cols = sheet.row_values(row)
                writer.writerow(cols)

        # load all sheets from the excel file,
        with open(map_filename, 'w') as m, open(nodes_filename, 'w') as r:
            for sheet in workbook.sheets():
                if 'node' in sheet.name.lower():
                    sheet_generator(sheet, r)
                else:
                    sheet_generator(sheet, m)


    def load_csv(self, map_filename, nodes_filename):
        """
        Read map data from a CSV file.
        """
        with open(map_filename, 'U') as m, open(nodes_filename, 'U') as r:
            self.load_map(csv.reader(m, delimiter='\t'))
            self.load_nodes(csv.reader(r, delimiter='\t'))


    def load_nodes(self, node_iterator):
        """
        Load the node data from an iterator.
        """
        # loop through node list, and attach titles and descriptions
        for row in node_iterator:

            if len(row) == 0:
                continue

            # check if exists
            if len(row) >= 1:
                node = row[0]
                if not node in self.nodes:
                    continue

            # load name
            if len(row) >= 2:
                self.nodes[node].name = row[1]

            # load description
            if len(row) >= 3:
                self.nodes[node].description = row[2]

            # load character spawn list
            if len(row) >= 4:
                for c in row[3].split():
                    obj_class = parser.object_table.first(c.lower())
                    if obj_class:
                        char = obj_class().move_to(self.nodes[node])

            # load object spawn list
            if len(row) >= 5:
                for o in row[4].split():
                    obj_class = parser.object_table.first(o.lower())
                    if obj_class:
                        self.nodes[node].objects.append(obj_class())


    def load_map(self, map_iterator):
        """
        Load the map data from an iterator.
        Process the map from top-left to bottom-right, row by row. Create nodes for IDs not yet
        encountered, and create links on the east, south and down end of sequences.
        """

        # store reference arrays to the last north and up cells
        north = []
        up = []
        n_blocking = []
        n_count = []

        for row in map_iterator:
            # store reference to the last west cell
            west = None
            w_blocking = False
            w_count = 0

            for x, node_id in enumerate(row):

                # expand north and up lists if required
                if len(north) <= x:
                    north.append(None)
                    n_blocking.append(False)
                    n_count.append(0)

                if len(up) <= x:
                    up.append(None)

                # test what kind of cell we are dealing with
                if re.match(r'[A-Z]+\d+', node_id):

                    # this is a node
                    # create it if it doesn't yet exist
                    node = self.nodes.get(node_id, Node(id=node_id))
                    self.nodes[node_id] = node

                    # check for exit references
                    # west reference is set, so make exits
                    # TODO: also make edge objects here
                    if west:
                        edge = Node(width=w_count)
                        if w_blocking:
                            edge.vision = SENS.KILL
                        edge.connect({DIR.WEST: west, DIR.EAST: node})
                        self.anonymous_nodes.append(edge)


                    # north reference is set, so make exits
                    # TODO: also make edge objects here
                    if north[x]:
                        edge = Node(height=n_count[x])
                        if n_blocking[x]:
                            edge.vision = SENS.KILL
                        edge.connect({DIR.NORTH: north[x], DIR.SOUTH: node})
                        self.anonymous_nodes.append(edge)


                    # up reference is set, so make exits
                    # TODO: also make edge objects here
                    elif up[x]:
                        # node.exits[DIR.UP]          = up[x]
                        # up[x].exits[DIR.DOWN]       = node
                        edge = Node(height=0)
                        edge.vision = SENS.KILL
                        edge.connect({DIR.UP: up[x], DIR.DOWN: node})
                        self.anonymous_nodes.append(edge)

                    # set north, west and up references to this node
                    west        = node
                    north[x]    = node
                    up[x]       = node
                    n_blocking[x]   = False
                    w_blocking      = False
                    n_count[x]  = 0
                    w_count     = 0

                elif node_id == '.' or node_id == '..':
                    # this is a horizontal link, so clear the up reference
                    up[x]           = None
                    n_blocking[x]   = False
                    w_blocking      = False
                    n_count[x]      += 1
                    w_count         += 1

                elif node_id == '%':
                    # TODO: one way, or door, needs logic here
                    up[x]           = None
                    n_blocking[x]   = True
                    w_blocking      = True
                    n_count[x]      = 0 # PORTAL
                    w_count         = 0 # PORTAL

                elif node_id == '|':
                    # this is a vertical link, so clear the north and west references
                    north[x]        = None
                    west            = None
                    n_blocking[x]   = False
                    w_blocking      = False
                    n_count[x]      = 0
                    w_count         = 0

                else:
                    # this is a blank cell, so clear all references
                    west            = None
                    north[x]        = None
                    up[x]           = None
                    n_blocking[x]   = False
                    w_blocking      = False
                    n_count[x]      = 0
                    w_count         = 0

        # sweet, we have a map.
