from enum import Enum

class Card(Enum):
    """ Card types """
    SNITCH = 1
    LOCKPICK = 2
    MUSCLE = 3
    LOOKOUT = 4
    DRIVER = 5
    CON_ARTIST = 6

    def __repr__(self):
        return self.name