from pwdlib import PasswordHash

pass_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pass_hash.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pass_hash.verify(password, password_hash)