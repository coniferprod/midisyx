import sys

from src.midisyx.message import Message
from src.midisyx.manufacturer import Manufacturer

def read_file_data(filename: str) -> bytes:
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            #print('Read {} bytes from file {}'.format(len(data), filename))
            return data
    except FileNotFoundError:
        print(f'File not found: {filename}')
        sys.exit(-1)

data = read_file_data(sys.argv[1])
print('File length = {} bytes'.format(len(data)))
message = Message(data)
print(message)

unknown_manufacturer = Manufacturer(bytes([0x44]))
print(unknown_manufacturer)
print(unknown_manufacturer.get_group())
