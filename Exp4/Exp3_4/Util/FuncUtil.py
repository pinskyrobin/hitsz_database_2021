import hashlib


def get_md5(data):
    m = hashlib.md5()
    b = data.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
