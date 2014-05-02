from texty.builtins import characters
from texty.builtins import commands
from texty.engine import obj
from texty.engine import server
from texty.engine.story import Story
from texty.engine.parser import parser
from texty.util.parsertools import VOCAB
from texty.util.serialize import dispatch
from tornado import escape
from tornado import ioloop
import collections
import itertools
import logging


class TextyEngine(object):
    """
    The Texty Engine is a multiplayer text adventure server. It is fully
    pluggable, and features natural language parsing and an adaptive AI.
    """

    options = {
        'tick_length': 750,    # 1.5 seconds per update tick
    }

    def __init__(self, storyname=None):
        """
        Initialize TextyEngine.
        """
        logging.info('Initializing Texty.')

        # TODO: find and parse config file
        # load the story
        Story.load(storyname)

        # create the websocket and HTTP server
        self.server = server.MUD()

        # player dict holds all connected players
        self.players = {}

        # ticks are periodic update intevals.
        self.tick = 0
        self.timer = ioloop.PeriodicCallback(self.update, self.options['tick_length'])

        # connect server event handlers
        self.server.on_connect = self.on_connect
        self.server.on_disconnect = self.on_disconnect
        self.server.on_read = self.on_read

        # conect server connection event handler
        server.Connection.on_write = self.on_write

        logging.info('')
        logging.info('Object Table:')
        logging.info('-------------')
        for i, o in enumerate(parser.object_table):
            logging.info('%03d:    %s', i, o.__name__)

        # create vocab table formatting strings
        cols = '| {:<10.10} | {:<14.14} | {:<12.12} | {:<10.10} |' #  | {:<10.10} |'
        vert = '+-{:<10.10}-+-{:<14.14}-+-{:<12.12}-+-{:<10.10}-+' # -+-{:<10.10}-+'
        rule = ['-' * 20] * 4

        logging.info('')
        logging.info(vert.format(*rule))
        logging.info(cols.format('VERBS', 'ADJECTIVES', 'NOUNS', 'PREPS')) # , 'CONFLICTS'))
        logging.info(vert.format(*rule))
        table = itertools.zip_longest(
            sorted(parser.command_table),
            sorted(VOCAB.adjectives | VOCAB.superlatives),
            sorted(VOCAB.nouns | VOCAB.reserved),
            sorted(VOCAB.prepositions) + \
                [rule[0], 'PHRASALS', rule[0]] + sorted(VOCAB.phrasals) + \
                [rule[0], 'ATTRIBUTES', rule[0]] + sorted(parser.attribute_table),
            # sorted(VOCAB.adjectives & VOCAB.nouns),
            fillvalue=''
        )
        for c in table:
            logging.info(cols.format(*c))
        logging.info(vert.format(*rule))


    def on_connect(self, connection, token):
        """
        Server reported a new connection.
        """
        # log connection
        logging.info('New connection from %s:%s on connection %d.' % (
            'ADDRESS',
            'PORT',
            connection.id))

        # create a player for this connection
        player = characters.Player(name='Player-%d' % connection.id, connection=connection)

        # and notify the story
        player = Story.get().on_player_connect(player)

        # assign it to the list
        self.players[connection.id] = player

        logging.info('TOKEN: %s' % token)

        # add players nouns to the vocab
        VOCAB.characters.update(player.nouns)

        # notify the player
        player.on_connect()

        # TODO: reconnect old players
        # player.on_reconnect()


    def on_disconnect(self, connection):
        """
        Server reported a disconnection
        """
        # log disconnection
        logging.info('Connection %d hungup.' % (connection.id))
        player = self.players[connection.id]
        # remove connection reference from player
        player.connection = None
        # notify the player
        player.on_disconnect()
        # notify the story
        Story.get().on_player_disconnect(player)

        # remove players name from the vocab
        VOCAB.characters.subtract(player.nouns)
        VOCAB.characters += collections.Counter()

        # remove player from player list
        # TODO: make sure that no rooms hold references to the player
        # at this point
        del self.players[connection.id]


    def on_read(self, connection, data):
        """
        Read data from a player connection.
        """
        # dispatch command to player
        player = self.players[connection.id]
        logging.info('%s: %s' % (player.name, data))

        player.do(data, echo=True)


    def on_write(self, data):
        """
        Hijack data and transform it into json messages for our custom client.
        """
        # transform strings into JSON
        data = escape.json_encode(dispatch(data))
        return data


    def run(self, address='127.0.0.1', port=4000):
        """
        start main game loop.
        """
        self.server.start(port)
        logging.info('Server started.')
        logging.info('Ready to rock on %s:%d.' % (address, port))
        self.timer.start()
        ioloop.IOLoop.instance().start()
        # NEVER REACHED


    def update(self):
        """
        Perform periodic game logic.
        """
        # increment counter
        self.tick += 1

        # tick the story
        Story.get().update(self.tick)

        # tick the players
        for p in self.players.values():
            p.update(self.tick)


    def shutdown(self):
        """
        """
        logging.info('Shutting down.')
        self.server.broadcast('B:Server is shutting down.')
        self.server.stop()
