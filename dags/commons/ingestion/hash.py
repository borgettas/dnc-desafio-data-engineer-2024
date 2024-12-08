import hashlib


def generate_hash(value: any):
    return hashlib.sha256(str(value).encode()).hexdigest()
