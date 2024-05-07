import time

from tqdm import tqdm


def countdown(t: int, message="Countdown", unit="seconds"):
    """
    Implements a countdown timer

    Args:
        t (int): The initial countdown time in the specified unit (e.g., seconds, minutes).
        message (str, optional): The message to display during the countdown.
                                Defaults to "Countdown".
        unit (str, optional): The unit of time for the countdown. Defaults to "seconds".
    """
    with tqdm(
        total=t, desc=message, unit=unit, bar_format="{desc}: {remaining}"
    ) as pbar:
        for _ in range(t):
            time.sleep(1)
            pbar.update(1)
