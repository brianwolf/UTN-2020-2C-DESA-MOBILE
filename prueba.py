

def hash_pass(hash_key: str, password: str) -> int:

    int_key = int.from_bytes(hash_key.encode('utf-8'), "big")
    int_pass = int.from_bytes(password.encode('utf-8'), "big")

    return int_pass + int_key


def des_hash_pass(hash_key: str, hash_pass: int) -> str:

    int_key = int.from_bytes(hash_key.encode('utf-8'), "big")
    int_hash = hash_pass - int_key

    return int_hash.to_bytes(64, 'big').decode('utf-8')


hash_key = "UTN"
password = "gordo atila"

pass_hash = hash_pass(hash_key, password)
pass_des_hash = des_hash_pass(hash_key, pass_hash)

print(password)
print(pass_hash)
print(pass_des_hash)
