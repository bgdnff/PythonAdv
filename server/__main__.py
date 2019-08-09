import yaml
import select
import socket
import logging
from argparse import ArgumentParser
import threading

from handlers import handle_default_request


def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except ConnectionResetError:
        if sock in connections:
            connections.remove(sock)
    except BlockingIOError:
        # происходят коллизии с записью в тот же сокет, просто подождем
        pass
    else:
        requests.append(bytes_request)


def write(sock, connection, response):
    try:
        sock.send(response)
    except Exception:
        if sock in connections:
            connections.remove(sock)


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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler(),
    ]
)

requests = []
connections = []

host, port = config.get('host'), config.get('port')

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(False)
    sock.settimeout(0)
    logging.info(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client was detected { address[0] }:{ address[1] }')
            connections.append(client)
        except:
            pass

        if len(connections) > 0:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )

            for read_client in rlist:
                read_thread = threading.Thread(
                    target=read, args=(read_client, connections, requests,
                                       config.get('buffersize'))
                )
                read_thread.start()

            if requests:
                bytes_request = requests.pop()
                bytes_response = handle_default_request(bytes_request)

                for write_client in wlist:
                    write_thread = threading.Thread(
                        target=write, args=(write_client, connections, bytes_response)
                    )
                    write_thread.start()

except KeyboardInterrupt:
    print('Server shutdown.')
