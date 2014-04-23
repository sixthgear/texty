# from tornado.platform.asyncio import AsyncIOMainLoop
# import asyncio

from tornado import ioloop
from tornado import escape

from texty.engine import server
from texty.engine.parser import parser
from texty.util.parsertools import VOCAB

from texty.builtins import commands
from texty.builtins import characters
from texty.builtins import story
from texty.builtins.objects import obj

import logging


class TextyEngine(object):
    """
    The Texty Engine is a multiplayer text adventure server. It is fully
    pluggable, and features natural language parsing and an adaptive AI.
    """

    options = {
        # 1.5 seconds per update tick
        'tick_length': 1500,
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
        logging.info('Command Table:')
        logging.info('--------------')
        for i, o in enumerate(parser.command_table.items()):
            logging.info('%03d:    %s', i, o)

        logging.info('')
        logging.info('Syntax Table:')
        logging.info('-------------')
        for i, o in enumerate(parser.syntax_table):
            logging.info('%03d:    %s', i, o)

        logging.info('')
        logging.info('Object Table:')
        logging.info('-------------')
        for i, o in enumerate(parser.object_table):
            logging.info('%03d:    %s', i, o)

        logging.info('')
        logging.info('Noun Table:')
        logging.info('--------------')
        for i, o in enumerate(VOCAB.nouns):
            logging.info(o)

        logging.info('')
        logging.info('Adjective Table:')
        logging.info('----------------')
        for i, o in enumerate(VOCAB.adjectives):
            logging.info(o)

        logging.info('')
        logging.info('Verb Table:')
        logging.info('----------------')
        for i, o in enumerate(VOCAB.verbs):
            logging.info(o)

        # logging.info('')
        # logging.info('Attribute Table:')
        # logging.info('----------------')
        # for i, o in enumerate(parser.attribute_table):
        #     logging.info(o)
        # logging.info('')


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

        # remove players first name to the vocab
        # VOCAB.characters -= player.nouns

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
        if isinstance(data, str):
            # broadcast
            if data.startswith('B:'):
                data = escape.json_encode({'type': 'broadcast', 'text': data[2:]})

            # conversation
            elif data.startswith('C:'):
                data = escape.json_encode({'type': 'conversation', 'items': [
                    {'icon': 'fa-quote-left', 'text': data[2:]},
                ]})

            # action
            elif data.startswith('A:'):
                data = escape.json_encode({'type': 'action', 'items': [
                    {'icon': 'fa-bolt', 'text': data[2:]},
                ]})

            # info
            elif data.startswith('I:'):
                data = escape.json_encode({'type': 'info', 'items': [
                    {'icon': 'fa-eye', 'text': data[2:]},
                ]})

            # other
            else:
                data = escape.json_encode({'type': 'action', 'items': [
                    {'text': data}
                ]})

        # or encode dicts
        elif isinstance(data, dict):
            data = escape.json_encode(data)

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
        # print (' [%04d] ...' % self.tick)

        # tick the story
        self.story.update(self.tick)

        # tick the combat
        ####


    def shutdown(self):
        logging.info('Shutting down.')
        self.server.broadcast('B:Server is shutting down.')
        self.server.stop()
