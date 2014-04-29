"""
objectlist.search('item')

    find and return the first matched object with keyword "item"

objectlist.search('item item2 item3 ...')
objectlist.search('item,item2,item3,...')
objectlist.search('item and item2 ...')

    find and return all specified items.

objectlist.search('n.item')
objectlist.search('second item')
objectlist.search('2nd item')

    find and return the nth matched object with keyword "item"

objectlist.search('n items')

    find and return the first n items that match keyword "item"

objectlist.search('all items')

    find and return all matched objects with keyword "item"

objectlist.search('all')

    find and return all objects

"""

from collections import OrderedDict

class ObjectList(list):
    """
    Collection that holds TextyObjects.
    Searchable on
    """
    def first(self, query, **kwargs):
        result = next(self.search(query, **kwargs), None)
        return result

    def search(self, query=None, terms=None, attribute=None, condition=None):
        results = self.__do_search(query, terms, attribute, condition)
        return results

    def __do_search(self, query=None, terms=None, attribute=None, condition=None):
        """
        Perform the keyword/attribute/condition lookup.
        This SUCKS in it's current form.
        """

        if isinstance(query, str):
            nouns = set((query,))
        elif hasattr(query, '__iter__'):
            nouns = set(query)
        elif query == None:
            nouns = None
        else:
            raise TypeError('ObjectList requires a string or iterable to search.')


        def search_objects(i):

            # found_noun = False
            if nouns and not nouns.issubset(i.nouns):
                return False

            # print adjectives, i.adjectives
            if terms and not set(terms).issubset(i.adjectives | i.nouns):
                return False

            if attribute and attribute not in i.attributes:
                return False

            if condition and not condition(i):
                return False

            return True

        return filter(search_objects, self)

    def __add__(self, rhs):
        return ObjectList(list.__add__(self, rhs))

    def append(self, value):
        # TODO: make sure objects has keyword attribute
        super(ObjectList, self).append(value)
