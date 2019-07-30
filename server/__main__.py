import yaml
import json
import socket
from argparse import ArgumentParser

from actions import resolve
from server.protocol import validate_request, make_response
# подключить относительные пути к модулям не получилось :(

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

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    print(f'Server started with { host }:{ port }')

    while True:
        client, address = sock.accept()
        print(f'Client was detected { address[0] }:{ address[1] }')

        b_request = client.recv(config.get('buffersize'))

        request = json.loads(b_request.decode())
        try:
            if validate_request(request):
                actions_name = request.get('action')
                controller = resolve(actions_name)
                if controller:
                    print(f'client send valid message {request}')
                    response = make_response(request.get('action'), 200, request.get('data'))
                else:
                    print(f'controller with action {actions_name} not found')
                    response = make_response(actions_name, 404, 'Action not found')

            else:
                print(f'Client send invalid message {request}')
                response = make_response(request.get('action'), 404, 'Wrong request')

        except Exception as err:
            print(f'Internal server error: {err}')
            response = make_response(request.get('action'), 500, 'Internal server error')

        str_response = json.dumps(response)
        client.send(str_response.encode())



        client.close()

except KeyboardInterrupt:
    print('Server shutdown.')
