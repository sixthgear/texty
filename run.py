#!/usr/bin/env python

if __name__ == '__main__':

    import sys
    import logging
    from optparse import OptionParser, OptionError
    from texty.engine import TextyEngine

    usage = 'usage: %prog [options] story'
    description = TextyEngine.__doc__

    parser = OptionParser(usage=usage, description=description)
    parser.add_option('-a', dest='address', help='IP address to bind to ', default='127.0.0.1')
    parser.add_option('-p', dest='port', help='port number to bind to', default=4000)

    try:
        (options, args) = parser.parse_args()
        story = args[0]
    except OptionError:
        sys.exit(2)
    except IndexError:
        print('No story specified')
        sys.exit(2)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='/tmp/texty.log',
        level=logging.DEBUG,
        filemode='w'
    )

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    sys.path.append('stories')

    g = TextyEngine(
        storyname=story
    )

    try:
        g.run(address=options.address, port=int(options.port))
    except (KeyboardInterrupt, SystemExit):
        g.shutdown()
        sys.exit(0)
