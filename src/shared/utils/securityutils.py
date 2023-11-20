import hashlib, binascii, os


def encrypt_user_password(password: str) -> str:
    salt = hashlib.sha256(os.urandom(32)).hexdigest().encode('ascii')
    # encode as ascii since hash will only contain 0-9 and a-z chars. Resulting lenght is 64bits
    return hash_sha_256(password, salt)


def safe_check_password(encrypted_password: str, clear_password: str) -> bool:
    salt = encrypted_password[:64]  # Retrieve stored salt
    verify_pwd = hash_sha_256(clear_password, salt.encode('ascii'))  # Hash clear_password with stored salt
    if len(encrypted_password) != len(verify_pwd):
        return False
    return encrypted_password == verify_pwd


def hash_sha_256(password: str, salt: bytes) -> str:
    m = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # 100000 is number of rounds recommended for SHA256. key lenght is 64bits
    m = binascii.hexlify(m)
    return (salt + m).decode('ascii')
