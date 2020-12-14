from flask import render_template
from flask_socketio import SocketIO

from CTFd.utils.decorators import admins_only
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from CTFd.plugins import register_plugin_assets_directory

import os


class WrappedChallenge():

    def __init__(self, inner, sio):
        self._c = inner
        self._sio = sio

    def __getattr__(self, val):
        return self._c.__getattribute__(self._c, val)

    @property
    def templates(self):
        return self._c.templates

    def create(self, request):
        return self._c.create(request)

    def read(self, challenge):
        return self._c.read(challenge)

    def update(self, challenge, request):
        return self._c.update(challenge, request)

    def delete(self, challenge):
        return self._c.delete(challenge)

    def attempt(self, challenge, request):
        status, msg = self._c.attempt(challenge, request)
        return status, msg

    def solve(self, user, team, challenge, request):
        data = {
            "user": user.name,
            "team": team.name if team else '',
            "chal": challenge.name,
            "pts": challenge.value
        }
        self._sio.emit('solve', data, broadcast=True)
        return self._c.solve(user, team, challenge, request)

    def fail(self, user, team, challenge, request):
        return self._c.fail(user, team, challenge, request)


def load(app):
    register_plugin_assets_directory(app, base_path='/plugins/toastee/assets/')

    sio = SocketIO()  # Server-side broadcast SocketIO

    # Route for the toast feed.
    @app.route('/toasts', methods=['GET'])
    def toasts():
        with open(os.path.dirname(os.path.realpath(__file__)) + '/assets/toastee.html', 'rb') as f:
            # Hacky workaround to keep the HTML in its own file...
            TEMPLATE = f.read().decode()
            return TEMPLATE

    @app.route('/toast', methods=['GET'])
    @admins_only
    def toast():
        import random
        data = {
            "user": 'Test',
            "team": '',
            "chal": 'Fake Challenge',
            "pts": random.randint(0, 50)
        }
        sio.emit('solve', data, broadcast=True)
        return 'OK'

    for (k, v) in CHALLENGE_CLASSES.items():
        CHALLENGE_CLASSES[k] = WrappedChallenge(v, sio)

    sio.init_app(app)
