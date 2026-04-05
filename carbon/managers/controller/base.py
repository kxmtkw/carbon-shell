

class BaseController:

    def __init__(self):
        pass

    def launch(self):
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError()