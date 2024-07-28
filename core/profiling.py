import inspect
import logging
from functools import wraps
from time import monotonic


def profileit(
    template="`{_function}` completed in {_time}.",
    level=logging.INFO,
    init_template=None,
    log_result=False,
):
    def decorator(func):
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # start the clock
            m = monotonic()
            func_failed = False
            # inspect the function being called with the args passed
            func_bound = signature.bind(*args, **kwargs)
            func_bound.apply_defaults()  # apply any defaults to the call (keywords not set)
            try:
                if init_template:
                    logging.getLogger(func.__module__).log(
                        level,
                        "profiling: "
                        + init_template.format(
                            # pass the positional values in
                            *func_bound.args,
                            # profiling information
                            _function=func.__name__,
                        ),
                    )
                # run the function
                result = func(*args, **kwargs)
                return result
            except Exception:
                func_failed = True
                raise
            finally:
                if not func_failed:
                    logging.getLogger(func.__module__).log(
                        level,
                        "profiling: "
                        + template.format(
                            # pass the positional values in
                            *func_bound.args,
                            # profiling information
                            _function=func.__name__,
                            _time=f"{monotonic() - m:.2f}s",
                            _result=result,
                        ),
                        extra={"details": result} if log_result else {},
                    )

        return wrapper

    return decorator
