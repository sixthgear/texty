from collections import deque
import itertools

class SyntaxTable(deque):
        
    def search_one(self, syntax):
        pass
        
    def search(self, syntax):
        pass
        
    def __do_search(self, syntax):
        """
        Perform the syntax lookup.
        """
        matches = list(self)

        for i in range(1, len(lookup) + 1):
            new_matches = []
            for m in matches:
                if lookup[:i] != m.__name__[:i]: 
                    # not a match: next key
                    continue
                elif lookup == m.__name__:
                    # exact match
                    return [m]
                else:
                    # partial match: check the next letter
                    new_matches.append(m)

            matches = new_matches[:]
            if len(matches) == 0:
                break

        return matches[:1]
        
        