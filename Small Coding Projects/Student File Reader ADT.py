# Implements the Bag ADT container using a Python list.

class GrabBag :
    # Constructs an empty bag.
    def __init__( self ):
        self._theItems = list()

    # Returns the number of items in the bag.
    def __len__( self ):
        return len( self._theItems )

    # Determines if an item is contained in the bag.
    def __contains__( self, item ):
        return item in self._theItems

    # Adds a new item to the bag.
    def add( self, item ):
        self._theItems.append( item )

    # Removes and returns an instance of the item from the bag.
    def grabItem(self):
        from random import choice
        item = choice(self._theItems)
        self._theItems.remove(item)
        return item 

    # Returns an iterator for traversing the list of items.
    def __iter__( self ):
        return _BagIterator( self._theItems)  # the iterator class lives in 
    
    # representation of the constructor 
    def __str__(self):
        return(f'{self._theItems}')


# An iterator for the Bag ADT implemented as a Python list.
class _BagIterator :
    def __init__( self, theList ):
        self._bagItems = theList     # an ALIAS to the bag's list (no copy)
        self._curItem = 0            # the slot it will hand out next

    def __iter__( self ):
        return self                  # an iterator's __iter__ always returns itself

    def __next__( self ):
        if self._curItem < len( self._bagItems ) :
            item = self._bagItems[ self._curItem ]
            self._curItem += 1
            return item
        else :
            raise StopIteration


dt = GrabBag()

dt.add('apple')
dt.add('computer')
dt.add('banana')

print(dt.grabItem())

print(dt)