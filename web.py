from tinyweb import webserver
from controller import Controller


def setup_web(w: webserver, c: Controller):
    w.add_resource(json_status(c), '/temps')
