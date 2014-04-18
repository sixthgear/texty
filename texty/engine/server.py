from texty.builtins import story
from tornado import web
from tornado import websocket
from tornado import ioloop
from tornado import httpserver
from tornado import template
import logging
import re

class HTMLClientHandler(web.RequestHandler):
    """
    This handler takes care of the HTML Client Application serving.
    """
    loader = template.Loader('texty/client-data/templates')

    def get(self):
        # serve base template
        s = story.Story.get()
        title = '%s %s' % (s.__name__, s.__version__)
        html = self.loader.load('base.html').generate(story=title)
        self.write(html)


class Connection(websocket.WebSocketHandler):
    """
    This simple handler wraps the tornado WebSocketHandler and hands off messages to our MUD server.
    """
    def open(self):
        self.application.MUD.connect(self)

    def on_message(self, data):
        self.application.MUD.data(self, data)

    def on_close(self):
        self.application.MUD.disconnect(self)

    def on_write(self, data):
        return data

    def send(self, data):
        data = self.on_write(data)
        return self.write_message(data)

    def write(self, data):
        logging.warning('Connection.write(data) is depracated. Use Conenction.send(data)')
        return self.write(data)


class MUD(object):

    # event handlers
    def on_connect(self, connection): pass
    def on_disconnect(self, connection): pass
    def on_read(self, connection, data): pass

    def __init__(self):
        # connection tracking
        self.connections = dict()
        self.serial = 0

        # tornado objects
        self.app = web.Application([
            (r'/', HTMLClientHandler),
            (r'/websocket', Connection),
        ])

        # add a reference to this object so we can access it from handlers
        self.app.MUD = self

    def start(self, port):
        """
        Start the server.
        """
        self.app.listen(port)

    def stop(self):
        pass

    def connect(self, connection):
        """
        Player has connected.
        """
        # set id to next serial and increment
        id = self.serial = self.serial + 1

        # save reference
        self.connections[id] = connection
        self.connections[id].id = id

        # fire event
        self.on_connect(connection)

    def disconnect(self, connection):
        """
        Player has disconnected.
        """
        # fire event
        self.on_disconnect(connection)

        # remove connection from list
        id = connection.id
        if id in self.connections:
            del self.connections[id]

    def data(self, connection, data):
        """
        Received data from a connection. Clean it up and pass it to application.
        """
        # truncate incoming data
        data = data[:100]
        # remove all but whitelisted characters
        data = re.sub('[^\w\d\-\?,.!:; ]', '', data)
        # fire event
        self.on_read(connection, data)


    def broadcast(self, message, exclude=None):
        """
        Broadcast a message to all connections.
        """
        if exclude == None:
            exclude = []
        for (id, connection) in self.connections.iteritems():
            if connection not in exclude:
                connection.send(message)
