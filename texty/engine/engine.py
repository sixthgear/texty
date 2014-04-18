from tornado import ioloop
from tornado import escape

from texty.engine import server
from texty.engine.parser import parser
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

        # ticks are periodic update intevals
        self.tick_length = 1500
        self.tick = 0
        self.timer = ioloop.PeriodicCallback(self.update, self.tick_length)

        # server event handlers
        self.server.on_connect = self.on_connect
        self.server.on_disconnect = self.on_disconnect
        self.server.on_read = self.on_read

        # override the connection on_write handler so we can add <p>tags</p>
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
        logging.info('Keyword Table:')
        logging.info('--------------')
        for i, o in enumerate(parser.keyword_table):
            logging.info(o)

        logging.info('')
        logging.info('Attribute Table:')
        logging.info('----------------')
        for i, o in enumerate(parser.attribute_table):
            logging.info(o)
        logging.info('')


    def on_connect(self, connection):
        """
        Server reported a new connection.
        """
        logging.info('New connection from %s:%s on connection %d.' % (
            'ADDRESS', #connection.address[0],
            'PORT', #connection.address[1],
            connection.id
        ))

        # create a temporary player for this connection
        p = characters.Player(name='Player-%d' % connection.id, connection=connection)

        # assign it to the list
        self.players[connection.id] = p

        # and notify the story
        self.story.on_player_connect(p)

        # TODO: reconnect old players

    def on_disconnect(self, connection):
        """
        Server reported a disconnection
        """
        logging.info('Connection %d hungup.' % (connection.id))

        # notify the story
        self.story.on_player_disconnect(self.players[connection.id])

        # remove player from player list
        del self.players[connection.id]

    def on_read(self, connection, data):
        p = self.players[connection.id]
        p.do(data, echo=True)

    def on_write(self, data):
        """
        Hijack data and transform it into json messages for our custom client.
        """
        if isinstance(data, basestring):
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
        # NEVER REACHED

    def update(self):
        self.tick += 1
        self.story.update(self.tick)
        print (' [%04d] ...' % self.tick)
        # self.server.broadcast(' >> tick %d' % self.tick)

    def shutdown(self):
        logging.info('Shutting down.')
        self.server.broadcast('B:Server is shutting down.')
        self.server.stop()
