class SearchDict(dict):
    """
    SearchDict is a dictionary-like object that is searchable.
    
    sd['fullkeyname']
    
        return the first object stored at this key
        
    sd['partialkeyna']
    
        search for, and return the first object stored at this key
        
    sd['2.keyname']

        return the second object stored at this key (or partial)
        
    sd['all.keyname']
    
        return all the objects stored at this keyname    
    """
        
    def __init__(self, items = None, quiet=True):
        
        super(SearchDict, self).__init__()
        
        if items:
            self.update(items)
            
        self.quiet = quiet

        # short wrapper around some super (dict) methods
        self._dict_contains = lambda key: \
            super(SearchDict,self).__contains__(key)

        self._dict_getitem = lambda key: \
            super(SearchDict,self).__getitem__(key)

                
    def _search(self, lookfor):
        
        if self._dict_contains(lookfor):
            return True, lookfor, self._dict_getitem(lookfor)
        
        matches = sorted(self.keys())

        for i in range(1, len(lookfor) + 1):            
            new_matches = []
            for key in matches:                
                if lookfor[:i] != key[:i]: continue # next key
                new_matches.append(key)            
            matches = new_matches[:]
                        
            if len(matches) == 0:
                return False, lookfor, False

        return True, lookfor, self._dict_getitem(matches[0])
    
    def __contains__(self, item):
        "Overides Dictionary __contains__ to use fuzzy matching"
        if self._search(item)[0]:
            return True
        else:
            return False

    def __getitem__(self, lookfor):
        "Overides Dictionary __getitem__ to use fuzzy matching"
        
        matched, key, item = self._search(lookfor)

        if not matched:
            if self.quiet: 
                return None
            else:
                raise KeyError()

        return item
    
