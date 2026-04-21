    

def main():
    
    from .core import CarbonCore

    try:
        core = CarbonCore()   
        core.init() 
    except Exception as e:
        from carbon.utils import logger
        logger.log(
            "main",
            f"{e.__class__.__name__}: {str(e)}",
            logger.Level.critical
        )
        logger.reportStartupError(
            "main",
            f"{e.__class__.__name__}: {str(e)}"
        )
        raise e


    try:
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