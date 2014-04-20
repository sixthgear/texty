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
        results = self.search(query, **kwargs)
        if results:
            return results[0]
        else:
            return None

    def search(self, query=None, adjectives=None, attribute=None, condition=None):
        results = self.__do_search(query, adjectives, attribute, condition)
        return results

    def __do_search(self, query=None, adjectives=None, attribute=None, condition=None):
        """
        Perform the keyword/attribute/condition lookup.
        This SUCKS in it's current form.
        """
        def search_objects(i):

            found_noun = False
            if query:
                for n in i.nouns:
                    if n.startswith(query):
                        found_noun = True
                        break
                if not found_noun:
                    return False

            # print adjectives, i.adjectives
            if adjectives and not set(adjectives).issubset(i.adjectives):
                return False

            if attribute and attribute not in i.attributes:
                return False

            if condition and not condition(i):
                return False

            return True

        return filter(search_objects, self)

    def append(self, value):
        # TODO: make sure objects has keyword attribute
        super(ObjectList, self).append(value)
