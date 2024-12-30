from controller import Controller


class WebController:
    def __init__(self, ctrl: Controller):
        self.c = ctrl

    def get(self, _) -> dict:
        return self.c.json_status()
