import json
import logging

from actions import resolve
from protocol import validate_request, make_response
from middlewares import compressing_middleware, encryption_middleware


@compressing_middleware
@encryption_middleware
def handle_default_request(bytes_request):
    request = json.loads(bytes_request.decode())
    try:
        if validate_request(request):
            actions_name = request.get('action')
            controller = resolve(actions_name)
            if controller:
                logging.info(f'client send valid message {request}')
                response = controller(request)
            else:
                logging.error(f'controller with action {actions_name} not found')
                response = make_response(actions_name, 404, 'Action not found')
        else:
            logging.error(f'Client send invalid message {request}')
            response = make_response(request.get('action'), 404, 'Wrong request')

    except Exception as err:
        logging.critical(f'Internal server error: {err}')
        response = make_response(request.get('action'), 500, 'Internal server error')

    str_response = json.dumps(response)
    return str_response.encode()
