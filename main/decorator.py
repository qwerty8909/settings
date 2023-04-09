'''
Декораторы могут использоваться в веб-приложениях для проверки авторизации пользователя,
перед тем как открывать ему доступ к функционалу. Они активно используются в веб-фреймворках Flask и Django.
Вот пример проверки авторизации на декораторах:
'''
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated