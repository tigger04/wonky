from types import SimpleNamespace


class Configs(SimpleNamespace):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattribute__(self, value):
        try:
            return super().__getattribute__(value)
        except AttributeError:
            return None
