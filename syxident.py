import sys

from midisyx.message import Message
from midisyx.manufacturer import Manufacturer

with open(sys.argv[1], 'rb') as f:
    data = f.read()

    print('File length = {} bytes'.format(len(data)))

    message = Message(data)
    print(message)

    print('Group: {}'.format(message.manufacturer.group))
