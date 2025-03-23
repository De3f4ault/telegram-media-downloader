import re
import math

def sanitize_filename(name: str) -> str:
    """Clean filenames for filesystem safety"""
    return re.sub(r'[^\w\-_\.]', '_', name).strip()

def format_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    if size_bytes == 0:
        return "0B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f"{size_bytes/p:.2f} {units[i]}"
