from protocol import make_response
from decorators import logged


@logged
def send_message(request):
    data = request.get('data')
    action = request.get('action')
    return make_response(action, 200, data)
