from typing import Tuple, Union, Optional
from enum import Enum, auto

DEVELOPMENT: int = 0x7D

class ManufacturerGroup(Enum):
    NORTH_AMERICAN = auto()
    EUROPEAN_AND_OTHER = auto()
    JAPANESE = auto()
    DEVELOPMENT = auto()

    def __str__(self) -> str:
        if self == ManufacturerGroup.NORTH_AMERICAN:
            return "North American"
        elif self == ManufacturerGroup.EUROPEAN_AND_OTHER:
            return "European & Other"
        elif self == ManufacturerGroup.JAPANESE:
            return "Japanese"
        elif self == ManufacturerGroup.DEVELOPMENT:
            return "Development"
        else:
            return "*unknown*"

class Manufacturer:
    def __init__(self, data: bytes):
        self.identifier = (data[0],)
        if self.identifier[0] == 0x00:
            self.identifier = (data[0], data[1], data[2])

    def __str__(self) -> str:
        s = '{} ('.format(self.get_name())
        for i in range(len(self.identifier)):
            s += '{0:02X}'.format(self.identifier[i])
            if i < len(self.identifier) - 1:
                s += ' '
        s += ')'
        return s

    def get_group(self) -> ManufacturerGroup:
        if self.identifier[0] == DEVELOPMENT:
            return ManufacturerGroup.DEVELOPMENT
        elif self.identifier[0] == 0x00:  # extended manufacturer ID
            if self.identifier[1] & (1 << 6) != 0:
                return ManufacturerGroup.JAPANESE
            elif self.identifier[1] & (1 << 5) != 0:
                return ManufacturerGroup.EUROPEAN_AND_OTHER
            else:
                return ManufacturerGroup.NORTH_AMERICAN
        else:
            if self.identifier[0] in range(0x01, 0x41):
                return ManufacturerGroup.NORTH_AMERICAN
            elif self.identifier[0] in range(0x40, 0x61):
                return ManufacturerGroup.JAPANESE
            else:
                return ManufacturerGroup.EUROPEAN_AND_OTHER

    def get_name(self) -> str:
        if self.identifier in MANUFACTURERS:
            return MANUFACTURERS[self.identifier]
        else:
            return '*unknown*'

MANUFACTURERS: dict[Tuple[int, ...], str] = {
    (0x01,): 'Sequential Circuits',
    (0x00, 0x00, 0x01): 'Time/Warner Interactive',
    (0x00, 0x00, 0x0E): 'Alesis Studio Electronics',
    (0x00, 0x20, 0x29): 'Focusrite/Novation',
    (0x40,): 'Kawai Musical Instruments MFG. CO. Ltd',
    (0x41,): 'Roland Corporation',
    (0x42,): 'Korg Inc.',
    (0x43,): 'Yamaha Corporation',
    (DEVELOPMENT,): 'Development/Non-commercial'
}

def find_manufacturer(identifier: Tuple[int, ...]) -> Optional[Manufacturer]:
    if identifier in MANUFACTURERS:
        return MANUFACTURERS[identifier]
    else:
        return None
