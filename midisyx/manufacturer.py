from typing import Tuple, Union, Optional
from enum import Enum, auto

class ManufacturerGroup(Enum):
    AMERICAN = auto()
    EUROPEAN_OR_OTHER = auto()
    JAPANESE = auto()
    DEVELOPMENT = auto()

class Manufacturer:
    def __init__(self, identifier: Tuple[int, ...], name: str, group: ManufacturerGroup):
        self.identifier = identifier
        self.name = name
        self.group = group

    def __str__(self) -> str:
        s = '{} ('.format(self.name)
        for i in range(len(self.identifier)):
            s += '{0:02X}'.format(self.identifier[i])
            if i < len(self.identifier) - 1:
                s += ' '
        s += ')'
        return s

MANUFACTURERS: dict[Tuple[int, ...], Tuple[str, ManufacturerGroup]] = {
    (0x01,): ('Sequential Circuits', ManufacturerGroup.AMERICAN),
    (0x00, 0x00, 0x01): ('Time/Warner Interactive', ManufacturerGroup.AMERICAN),
    (0x00, 0x00, 0x0E): ('Alesis Studio Electronics', ManufacturerGroup.AMERICAN),
    (0x00, 0x20, 0x29): ('Focusrite/Novation', ManufacturerGroup.EUROPEAN_OR_OTHER),
    (0x40,): ('Kawai Musical Instruments MFG. CO. Ltd', ManufacturerGroup.JAPANESE),
    (0x41,): ('Roland Corporation', ManufacturerGroup.JAPANESE),
    (0x42,): ('Korg Inc.', ManufacturerGroup.JAPANESE),
    (0x43,): ('Yamaha Corporation', ManufacturerGroup.JAPANESE),
}

def find_manufacturer(identifier: Tuple[int, ...]) -> Optional[Manufacturer]:
    if identifier in MANUFACTURERS:
        manuf = MANUFACTURERS[identifier]
        return Manufacturer(identifier, manuf[0], manuf[1])
    else:
        return None

