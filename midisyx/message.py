from enum import Enum, auto

from midisyx.manufacturer import find_manufacturer

class MessageKind(Enum):
    DEVELOPMENT = auto()
    UNIVERSAL = auto()
    MANUFACTURER = auto()

INITIATOR = 0xf0
TERMINATOR = 0xf7

class Message:
    def __init__(self, data: bytes):
        if len(data) < 4:
            raise ValueError('Not enough data for a valid MIDI System Exclusive message')
        if data[0] != INITIATOR and data[-1] != TERMINATOR:
            raise ValueError('Not a valid MIDI System Exclusive message')

        if data[1] == 0x7d:
            self.kind = MessageKind.DEVELOPMENT
            self.payload = data[2 : -1]
        elif data[1] == 0x7e:
            self.kind = MessageKind.UNIVERSAL
            self.is_realtime = False
            self.sub_id1 = data[2]
            self.sub_id2 = data[3]
            self.payload = data[4 : -1]
        elif data[1] == 0x7f:
            self.kind = MessageKind.UNIVERSAL
            self.is_realtime = True
            self.sub_id1 = data[2]
            self.sub_id2 = data[3]
            self.payload = data[4 : -1]
        elif data[1] == 0x00:  # extended manufacturer
            self.kind = MessageKind.MANUFACTURER
            self.manufacturer = find_manufacturer((data[1], data[2], data[3]))
            self.payload = data[4 : -1]
        else: # standard one-byte manufacturer
            self.kind = MessageKind.MANUFACTURER
            # Removed the type annotation from this second `manufacturer`,
            # and mypy is happy again.
            self.manufacturer = find_manufacturer((data[1],))  # initialize with one-element tuple
            self.payload = data[2 : -1]

    def __str__(self) -> str:
        s = ''
        if self.kind == MessageKind.DEVELOPMENT:
            s += 'Development/Non-commercial'
            s += '  Payload: {0} bytes'.format(len(self.payload))
        elif self.kind == MessageKind.UNIVERSAL:
            s += 'Universal, '
            if self.is_realtime:
                s += 'real-time'
            else:
                s += 'non-real-time'
            s += '  Sub-ID 1 = {0:02X}H  Sub-ID 2 = {1:02X}H'.format(self.sub_id1, self.sub_id2)
            s += '  Payload: {0} bytes'.format(len(self.payload))
        elif self.kind == MessageKind.MANUFACTURER:
            s += 'Manufacturer: '
            s += '(unknown)' if self.manufacturer is None else '{}'.format(self.manufacturer)
            s += '  Payload: {0} bytes'.format(len(self.payload))
        return s
