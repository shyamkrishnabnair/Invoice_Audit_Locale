from pathlib import Path
from queue import Queue

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class InvoiceFileHandler(FileSystemEventHandler):

    def __init__(self, file_queue: Queue):
        self.file_queue = file_queue

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        print(
            f"[MONITOR] New file detected: {file_path}",
            flush=True,
        )

        self.file_queue.put(file_path)


def start_watcher(
    directory: str,
    file_queue: Queue,
) -> Observer:

    path = Path(directory)

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    event_handler = InvoiceFileHandler(file_queue)

    observer = Observer()

    observer.schedule(
        event_handler,
        str(path),
        recursive=False,
    )

    observer.start()

    print(
        f"[MONITOR] Watching directory: {path}",
        flush=True,
    )

    return observer