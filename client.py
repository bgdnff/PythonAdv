import zlib
import yaml
import json
import socket
from datetime import datetime
from argparse import ArgumentParser


WRITE_MODE = 'write'
READ_MODE = 'read'


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

parser.add_argument(
    '-m', '--mode', type=str, default=WRITE_MODE,
    help='Sets client mode'
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
    print('Client was started')

    while action != 'quit':
        if args.mode == WRITE_MODE:
            action = input('Enter action')
            data = input('Enter data: ')
            request = make_request(action, data)
            request_str = json.dumps(request)
            bytes_request = zlib.compress(request_str.encode())

            sock.send(bytes_request)
            print(f'Client send data { data }')
        elif args.mode == READ_MODE:
            print('listening...')
            response = sock.recv(config.get('buffersize'))
            bytes_response = zlib.decompress(response)
            print(f'Server send data { bytes_response.decode() }')
        else:
            print('wrong mode parameter')
            break
    print('client quited')
except KeyboardInterrupt:
    print('client shutdown.')
