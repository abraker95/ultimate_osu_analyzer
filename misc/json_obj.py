
class JsonObj:

    def __init__(self, params={}):
        self.json(params)


    def __repr__(self):
        try: return self.name
        except AttributeError:
            return super().__repr__()


    def json(self, params={}):
        if params:
            for param in params:
                setattr(self, param, params[param])
            return None
        else:
            d = {}
            members = [ attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") ]
            for member in members:
                d.update({ member: getattr(self, member) })
            return d