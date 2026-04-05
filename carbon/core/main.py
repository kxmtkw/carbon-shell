


def main():
    
    from .core import CarbonCore

    try:
        core = CarbonCore()
        core.run()
    except KeyboardInterrupt:
        core.shutdown()
    except Exception as e:
        core.shutdown()
        raise e