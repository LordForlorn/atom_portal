import hashlib


username = "TestUsername"
password = "password123"

def hash_md5(value): return hashlib.md5((value).encode()).hexdigest()

print(hash_md5(username+password))
