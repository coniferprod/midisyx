from email.message import Message
import sys

from midisyx.message import Message

with open(sys.argv[1], 'rb') as f:
    data = f.read()

    print('File length = {} bytes'.format(len(data)))

    message = Message(data)
    print(message)
