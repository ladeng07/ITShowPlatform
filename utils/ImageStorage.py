from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os, time, random,hashlib
from django.http import HttpResponse


class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)
    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        md5hash = hashlib.md5((os.path.basename(name) + str(time.time())).encode("utf-8"))
        fn = md5hash.hexdigest()
        name = os.path.join(d, fn + ext)
        return super(ImageStorage, self)._save(name, content)
