from typing import Tuple, Optional
from enum import Enum, auto

class Group(Enum):
    NORTH_AMERICAN = auto()
    EUROPEAN_OR_OTHER = auto()
    JAPANESE = auto()
    DEVELOPMENT = auto()

    def __str__(self) -> str:
        if self == Group.NORTH_AMERICAN:
            return "North American"
        elif self == Group.EUROPEAN_OR_OTHER:
            return "European or Other"
        elif self == Group.JAPANESE:
            return "Japanese"
        else:
            return "Development"

class Manufacturer:
    def __init__(self, identifier: Tuple[int, ...]):
        if not identifier in self._names:
            raise ValueError('Unknown manufacturer identifier')
        self.identifier = identifier

    def __str__(self) -> str:
        s = '{} ('.format(self.name)
        for i in range(len(self.identifier)):
            s += '{0:02X}'.format(self.identifier[i])
            if i < len(self.identifier) - 1:
                s += ' '
        s += ')'
        return s

    @property
    def group(self) -> Group:
        # Handle the standard one-byte identifiers first.
        if len(self.identifier) == 1:
            if 0x01 <= self.identifier[0] <= 0x3F:
                return Group.NORTH_AMERICAN
            elif 0x40 <= self.identifier[0] <= 0x5F:
                return Group.JAPANESE
            # Looks like there are no identifiers assigned from 60H to 7FH
        else: # extended three-byte identifier, look at the second byte
            if 0x00 <= self.identifier[1] <= 0x02:
                return Group.NORTH_AMERICAN
            elif 0x20 <= self.identifier[1] <= 0x21:
                return Group.EUROPEAN_OR_OTHER
            elif 0x40 <= self.identifier[1] <= 0x4F:
                return Group.JAPANESE

        return Group.DEVELOPMENT

    @property
    def name(self) -> str:
        # identifier is valid or unless this instance would not exist
        return self._names[self.identifier]

    _names: dict[Tuple[int, ...], str] = {
        (0x01,): 'Sequential Circuits',
        (0x00, 0x00, 0x01): 'Time/Warner Interactive',
        (0x00, 0x00, 0x0E): 'Alesis Studio Electronics',
        (0x00, 0x20, 0x29): 'Focusrite/Novation',
        (0x40,): 'Kawai Musical Instruments MFG. CO. Ltd',
        (0x41,): 'Roland Corporation',
        (0x42,): 'Korg Inc.',
        (0x43,): 'Yamaha Corporation',
    }

# Some pre-made manufacturers:
kawai = Manufacturer((0x40,))
roland = Manufacturer((0x41,))
korg = Manufacturer((0x42,))
yamaha = Manufacturer((0x43,))
