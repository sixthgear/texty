from collections import Counter, OrderedDict

def levenshtein(s, t):
    """
    Calcutates the Levenshtein distance between two strings.
    """
    m = len(s) + 1
    n = len(t) + 1
    d = [[0 for j in range(n)] for i in range(m)]

    for i in range(m):
        # the distance of any first string to an empty second string
        d[i][0] = i
    for j in range(n):
        # the distance of any second string to an empty first string
        d[0][j] = j

    for j in range(1, n):
        for i in range(1, m):
            if s[i-1] == t[j-1]:
                # no operation required
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min (
                    # a deletion
                    d[i-1][j] + 1,
                    # an insertion
                    d[i][j-1] + 1,
                    # a substitution
                    d[i-1][j-1] + 1
                )
    return d[m-1][n-1]


class FuzzyDict(OrderedDict):

    def __init__(self, *args):
        OrderedDict.__init__(self, *args)
        self.max_distance = 2
        self.max_results = 1

    def search(self, key):
        """
        Perform a fuzzy search for item [key].
        Returns a tuple of:
        - (True, value)             if a match was found
        - (False, [key, key...])    if a partial match was found
        - (False, [])               if no suitable matches could be found
        """

        # check for exact match
        if key in self:
            return (True, self[key])

        # counter used to hold levenshtein distances
        c = Counter()

        for potential in self.keys():

            # check for prefix match, count this as a complete match
            if potential.startswith(key):
                return (True, self[potential])

            # calculate the levenshtein distance between each key
            # this kind of sucks
            dist = levenshtein(key, potential)
            if dist <= self.max_distance:
                # add potential to the counter
                c[potential] = dist

        if c:

            # get the closest [max_results] matches and return them
            closest_matches = [k[0] for k in c.most_common()[-self.max_results:]]
            closest_matches.reverse()
            return False, closest_matches

        return (False, [])

