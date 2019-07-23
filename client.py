import yaml
import socket
from argparse import ArgumentParser


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

data = ''

print('type "quit" to quit')

try:
    while data != 'quit':
        data = input('Enter data: ')
        try:
            sock = socket.socket()
            sock.connect((host, port))
            print('Connected to server')

            sock.send(data.encode())
            print(f'Client send data { data }')

            b_response = sock.recv(config.get('buffersize'))
            print(f'Server send data { b_response.decode() }')
        except ConnectionRefusedError:
            print ('no connection to server')


    print('client quited')
except KeyboardInterrupt:
    print('client shutdown.')