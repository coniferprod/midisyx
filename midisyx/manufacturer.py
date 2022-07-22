from typing import Tuple, Optional
from enum import Enum, auto

class Group(Enum):
    AMERICAN = auto()
    EUROPEAN_OR_OTHER = auto()
    JAPANESE = auto()
    DEVELOPMENT = auto()

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
