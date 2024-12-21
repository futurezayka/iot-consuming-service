import asyncio


def retry(max_retries: int, delay: int = 2):
    """Retry decorator to handle retries for asynchronous functions."""

    def decorator(func):
        # noinspection PyBroadException
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay**attempt)

        return wrapper

    return decorator
