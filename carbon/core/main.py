


def main():
    
    from .core import CarbonCore

    core = CarbonCore()        

    try:
        core.init()
        core.run()
    except KeyboardInterrupt:
        m = core.shutdown()
        print(m)
    except Exception as e:

        from carbon.utils import logger

        logger.log(
            "main",
            f"{e.__class__.__name__}: {str(e)}",
            logger.Level.critical
        )

        core.shutdown()
        raise e