from pathlib import Path

from app.audit.repository import (
    checksum_exists,
    create_invoice_record,
)
from app.monitor.checksum import calculate_checksum
from app.monitor.stability import wait_for_file_stability


def process_file(file_path: Path) -> None:
    print(
        f"[PROCESSOR] Processing: {file_path}",
        flush=True,
    )

    stable = wait_for_file_stability(file_path)

    if not stable:
        print(
            f"[PROCESSOR] File did not become stable: {file_path}",
            flush=True,
        )
        return

    checksum = calculate_checksum(file_path)

    print(
        f"[PROCESSOR] SHA-256: {checksum}",
        flush=True,
    )

    if checksum_exists(checksum):
        print(
            f"[PROCESSOR] Duplicate skipped: {file_path}",
            flush=True,
        )
        return

    invoice_id = create_invoice_record(
        file_path=str(file_path),
        file_checksum=checksum,
    )

    print(
        f"[PROCESSOR] Invoice registered: {invoice_id}",
        flush=True,
    )

    # LangGraph processing will be triggered here later.