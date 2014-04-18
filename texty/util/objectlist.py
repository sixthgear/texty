"""
objectlist.seach('item')

    find and return the first matched object with keyword "item"
    
objectlist.seach('item item2 item3 ...')
objectlist.seach('item,item2,item3,...')
objectlist.seach('item and item2 ...')

    find and return all specified items.
                
objectlist.seach('n.item')
objectlist.seach('second item')
objectlist.seach('2nd item')
        
    find and return the nth matched object with keyword "item"
    
objectlist.seach('n items')
    
    find and return the first n items that match keyword "item"
    
objectlist.seach('all items')

    find and return all matched objects with keyword "item"
    
objectlist.seach('all')

    find and return all objects
    
"""

from collections import OrderedDict

class ObjectList(list):
    """
    Collection that holds TextyObjects.
    Searchable on
    """        
    def search_one(self, lookup):
        results = self.search(lookup)
        if results:
            return results[0]
        else:
            return None
        
    def search(self, query=None, attribute=None, condition=None):                
        results = self.__do_search(query, attribute, condition)
        return results
                
    def __do_search(self, keyword=None, attribute=None, condition=None):
        """
        Perform the keyword/attribute/condition lookup.
        This SUCKS in it's current form.
        """
        def search_objects(i):
            
            found_keyword = False
            found_attribute = False
            found_condition = False
            
            if keyword:
                for k in i.keywords:
                    if k.startswith(keyword):
                        found_keyword = True
                        break
                if not found_keyword:
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