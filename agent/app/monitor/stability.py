import time
from pathlib import Path


def wait_for_file_stability(
    file_path: Path,
    interval: float = 1.0,
    stable_checks: int = 2,
    timeout: float = 60.0,
) -> bool:
    """
    Wait until a file's size stops changing.

    Returns True when the file is considered stable.
    Returns False if the timeout is reached.
    """

    start_time = time.monotonic()
    previous_size = None
    stable_count = 0

    while time.monotonic() - start_time < timeout:
        if not file_path.exists():
            return False

        current_size = file_path.stat().st_size

        if current_size == previous_size:
            stable_count += 1

            if stable_count >= stable_checks:
                return True
        else:
            stable_count = 0
            previous_size = current_size

        time.sleep(interval)

    return False