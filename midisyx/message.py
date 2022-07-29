from enum import Enum, auto

from midisyx.manufacturer import Manufacturer

class Kind(Enum):
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

        self.manufacturer = None

        if data[1] == 0x7d:
            self.kind = Kind.DEVELOPMENT
            self.payload = data[2:-1]
        elif data[1] == 0x7e or data[1] == 0x7f:
            self.kind = Kind.UNIVERSAL
            self.sub_id1 = data[2]
            self.sub_id2 = data[3]
            self.payload = data[4:-1]
            self.is_realtime = True if data[1] == 0x7f else False
        elif data[1] == 0x00:  # extended manufacturer
            self.kind = Kind.MANUFACTURER
            try:
                # Initialize manufacturer with tuple of three bytes:
                self.manufacturer = Manufacturer((data[1], data[2], data[3]))
            except:
                raise
            self.payload = data[4:-1]
        else: # standard one-byte manufacturer
            self.kind = Kind.MANUFACTURER
            try:
                # Initialize with one-byte tuple:
                self.manufacturer = Manufacturer((data[1],))
            except:
                raise
            self.payload = data[2:-1]

    def __str__(self) -> str:
        s = ''
        if self.kind == Kind.DEVELOPMENT:
            s += 'Development/Non-commercial'
            s += '  Payload: {0} bytes'.format(len(self.payload))
        elif self.kind == Kind.UNIVERSAL:
            s += 'Universal, '
            if self.is_realtime:
                s += 'real-time'
            else:
                s += 'non-real-time'
            s += '  Sub-ID 1 = {0:02X}H  Sub-ID 2 = {1:02X}H'.format(self.sub_id1, self.sub_id2)
            s += '  Payload: {0} bytes'.format(len(self.payload))
        elif self.kind == Kind.MANUFACTURER:
            s += 'Manufacturer: '
            s += '(unknown)' if self.manufacturer is None else '{}'.format(self.manufacturer)
            s += '\nPayload: {0} bytes'.format(len(self.payload))
        return s
