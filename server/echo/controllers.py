from protocol import make_response


def get_echo(request):
    data = request.get('data')
    action = request.get('action')
    return make_response(action, 200, data)
