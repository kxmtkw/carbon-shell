


def main():
    
    from .core import CarbonCore

    try:
        core = CarbonCore()
        core.run()
    except KeyboardInterrupt:
        print(core.shutdown())
    except Exception as e:

        from carbon.utils import notify
        notify(
            "Error!",
            f"{e.__class__.__name__}: {str(e)}",
            urgency="critical",
            timeout=-1
        )

        core.shutdown()
        raise e