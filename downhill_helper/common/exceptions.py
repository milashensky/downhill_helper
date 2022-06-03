class CommonException(Exception):
    message = ""

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.message = args[0]
        for key, val in kwargs.items():
            setattr(self, key, val)
        return super().__init__(self.message)


class PutMethodNotFound(Exception):

    def __init__(self, action, name):
        super().__init__('Method "put_%s" not found in "%s"' % (action, name))
