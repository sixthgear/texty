from texty.engine.map import Map
import sys
import importlib
import logging

class Story(object):
    """
    Base Story object.
    """
    __name__ = ''
    __version__ = '0.0.0'
    loaded_story = None

    def __init__(self):
        # perform map loading
        self.map = Map()

        excel_file  = self.options.get('excel_file')
        map_file    = self.options.get('map_file')
        room_file   = self.options.get('room_file')


        # if excel file defined use it to write out the csv files.
        if excel_file:
            try:
                self.map.load_excel(excel_file, map_file, room_file)
            except ImportError as e:
                logging.info('No xlrd module found, loading from CSV.')
            except FileNotFoundError as e:
                logging.info('Excel file not found, loading from CSV.')
            finally:
                self.map.load_csv(map_file, room_file)

        else:
            self.map.load_csv(map_file, room_file)

        self.starting_room = self.map.rooms[self.options.get('start_at')]
        # call initialize
        self.initialize()

    def initialize(self):
        pass

    def on_player_connect(self, player):
        pass

    def on_player_disconnect(self, player):
        pass

    def update(self, tick):
        pass

    @classmethod
    def load(cls, story):
        """
        Try to load a story from disk.
        """
        try:
            story_module = importlib.import_module(story)
            cls.loaded_story = story_module.storyclass()
            logging.info('Story "%s" %s loaded.' % (cls.loaded_story.__name__, cls.loaded_story.__version__))
            return cls.loaded_story

        except ImportError: # , AttributeError
            print('Couldn\'t find story %s' % story, file=sys.stderr)
            sys.exit()

    @classmethod
    def get(cls):
        """
        Get a reference to the currently loaded story.
        """
        return cls.loaded_story

        # TODO: validate story
        # TODO: compile json files

        # """
        # Given the current list of room descriptions, characters and objects, create
        # A series of static JSON documents that the client can load and cache so
        # that we don't have to send verbose descriptions of each object every time
        # the client asks for it. We can simply send an lookup ID.
        # """
