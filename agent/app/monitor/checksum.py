from hashlib import sha256
from pathlib import Path

def calculate_checksum(file_path: Path) -> str:

    hasher = sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(1024*1024):
            hasher.update(chunk)


    return hasher.hexdigest()

