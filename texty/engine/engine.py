# from tornado.platform.asyncio import AsyncIOMainLoop
# import asyncio

from tornado import ioloop
from tornado import escape

from texty.engine import server
from texty.engine.parser import parser
from texty.util.parsertools import VOCAB
from texty.util.serialize import dispatch

from texty.builtins import commands
from texty.builtins import characters
from texty.builtins import story
from texty.builtins.objects import obj

import itertools
import collections
import logging


class TextyEngine(object):
    """
    The Texty Engine is a multiplayer text adventure server. It is fully
    pluggable, and features natural language parsing and an adaptive AI.
    """

    options = {
        'tick_length': 1500,    # 1.5 seconds per update tick
    }

    def __init__(self, storyname=None):
        """
        Initialize TextyEngine.
        """
        logging.info('Initializing Texty.')

        # TODO: find and parse config file
        # load the story
        self.story = story.Story.load(storyname)

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
        cols = '| {:<10.10} | {:<6.6} | {:<14.14} | {:<12.12} | {:<10.10} | {:<10.10} |'
        vert = '+-{:<10.10}-+-{:<6.6}-+-{:<14.14}-+-{:<12.12}-+-{:<10.10}-+-{:<10.10}-+'
        rule = ['-'*20] * 6

        logging.info('')
        logging.info(vert.format(*rule))
        logging.info(cols.format('VERBS', 'PHRASE', 'ADJECTIVES', 'NOUNS', 'PREPS', 'ATTRIBUTES'))
        logging.info(vert.format(*rule))
        table = itertools.zip_longest(
            sorted(parser.command_table),
            sorted(VOCAB.phrasals),
            sorted(VOCAB.adjectives | VOCAB.superlatives),
            sorted(VOCAB.nouns | VOCAB.reserved),
            sorted(VOCAB.prepositions),
            sorted(parser.attribute_table),
            fillvalue=''
        )
        for c in table:
            logging.info(cols.format(*c))
        logging.info(vert.format(*rule))


    def on_connect(self, connection):
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
        player = self.story.on_player_connect(player)

        # assign it to the list
        self.players[connection.id] = player

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
        self.story.on_player_disconnect(player)

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
        # AsyncIOMainLoop().install()
        # asyncio.get_event_loop().run_forever()
        # NEVER REACHED


    def update(self):
        """
        Perform periodic game logic.
        """
        # increment counter
        self.tick += 1
        # tick the story
        self.story.update(self.tick)
        # tick the combat
        ####


    def shutdown(self):
        logging.info('Shutting down.')
        self.server.broadcast('B:Server is shutting down.')
        self.server.stop()
