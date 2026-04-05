from threading import Lock
    
def locked(lock: Lock = None):

    def decorator(method):

        if decorator.lock is None:
            decorator.lock = Lock()

        def wrapper(*args, **kwargs):
            with decorator.lock:
                ret = method(*args, **kwargs)
            return ret
            
        return wrapper
    
    decorator.lock = lock

    return decorator