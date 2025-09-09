import os
import uuid


def generate_filename(prefix, filename, name=None):
    prefix = prefix.lstrip('/')
    file_ext = os.path.splitext(filename)[1]
    if not name:
        return f"{prefix}/{uuid.uuid4()}{file_ext}"
    else:
        return f"{prefix}/{name}{file_ext}"
