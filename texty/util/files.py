import os
import random

def random_line(filename):
    """
    Generator to open a large file and yield random lines from it.
    This should be very memory efficent and quick, since we do
    not read the whole file, just seek to a random spot and return
    the next full line.
    """
    used = set()
    with open(filename,'r') as file:
        size = os.stat(filename)[6]
        while True:
            # pick a random byte from the file, wrap around to file size
            n = random.randint(0, size-1) % size
            file.seek(n)

            # read a dummy line. We do this to make sure that our random seek
            # didn't stick us in the middle of a line.
            file.readline()
            line = file.readline().strip()

            # loop until we hit an unused line
            # TODO: this may fail if the loop hits the EOF
            while line in used:
                line = file.readline().strip()
                if line == '':
                    file.seek(0)
                    line = file.readline().strip()

            # remember this line so we don't yield it again.
            used.add(line)
            yield line

def construct_name(gender=None):

    gender = gender or random.choice(['M', 'F'])
    if gender == 'M':
        first = next(random_line('texty/data/male.txt'))
    else:
        first = next(random_line('texty/data/female.txt'))

    family = next(random_line('texty/data/family.txt'))
    return '%s %s' % (first, family)

def construct_occupation():
    return next(random_line('texty/data/occupations.txt'))

