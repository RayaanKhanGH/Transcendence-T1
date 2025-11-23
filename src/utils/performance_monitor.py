import functools

# No-op performance monitor (psutil removed)
def monitor_performance(step_name: str):
    """Decorator that does nothing – kept for compatibility.
    It simply returns the original function unchanged.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
