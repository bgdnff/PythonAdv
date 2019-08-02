from datetime import datetime


def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    return False


def make_response(action, code, data=None):
    # мне кажется тут должен быть именно action, а не весь реквест
    return {'action': action,
            'time': datetime.now().timestamp(),
            'code': code,
            'data': data}
