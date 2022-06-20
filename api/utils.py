import hashlib
import os
from time import time


def image_upload_path(instance, filename):
    # creating a path from an incoming image file uploaded using either the model's primary key or uuid field to generate a random hash string
    # <base folder for user uploads>/<django model object for image>/<a-zA-Z0-9>/<a-zA-Z0-9>/<a-zA-Z0-9>/filename
    # examples:
    # uploads/recipes/e3/2S/23/b655f20638017e6306fd1ca8cc9244d3.jpg.jpg
    (file_name, file_ext) = os.path.splitext(filename)
    strclass = str(instance.__class__.__name__).lower()

    instance_id = hasattr(instance, 'uuid') and instance.uuid or hasattr(instance, 'id') and instance.id or None
    if not bool(instance_id): raise Exception('Upload failed due to missing model id')

    strtime = str(time()).encode("utf-8")
    strpk = str(instance_id).encode("utf-8")
    hashed_path = hashlib.md5(strpk).hexdigest()
    hashed_name = hashlib.md5(strpk+strtime).hexdigest()
    hashed_name = ''.join([hashed_name, file_ext])
    return os.path.normpath(os.path.join(strclass, hashed_path[0:2], hashed_path[2:4], hashed_path[4:6], hashed_name))
