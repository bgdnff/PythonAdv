import zlib
import yaml
import json
import socket
from datetime import datetime
from argparse import ArgumentParser
import threading


WRITE_MODE = 'write'
READ_MODE = 'read'


def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)
        bytes_response = zlib.decompress(response)
        print(bytes_response.decode())


def make_request(action, data):
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)


args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

host, port = config.get('host'), config.get('port')

action = ''

print('type "quit" to quit')

try:
    sock = socket.socket()
    sock.connect((host, port))

    read_thread = threading.Thread(
        target=read, args=(sock, config.get('buffersize'))
    )
    read_thread.start()

    print('Client was started')

    while action != 'quit':

        action = input('Enter action')
        data = input('Enter data: ')
        request = make_request(action, data)
        request_str = json.dumps(request)
        bytes_request = zlib.compress(request_str.encode())

        sock.send(bytes_request)
        print(f'Client send data { data }')

    print('client quited')
except KeyboardInterrupt:
    print('client shutdown.')
