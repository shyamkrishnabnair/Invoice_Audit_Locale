from contextlib import asynccontextmanager
from queue import Queue
from threading import Thread

from fastapi import FastAPI

from app.monitor.processor import process_file
from app.monitor.watcher import start_watcher


INCOMING_DIR = "/app/data/incoming"


file_queue = Queue()


def worker():
    while True:
        file_path = file_queue.get()

        try:
            process_file(file_path)
        except Exception as exc:
            print(
                f"[PROCESSOR] Failed to process {file_path}: {exc}",
                flush=True,
            )
        finally:
            file_queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):

    worker_thread = Thread(
        target=worker,
        daemon=True,
    )
    worker_thread.start()

    observer = start_watcher(
        INCOMING_DIR,
        file_queue,
    )

    yield

    observer.stop()
    observer.join()


app = FastAPI(
    title="AI Invoice Auditor Agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "agent",
    }