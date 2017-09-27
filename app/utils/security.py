import random
import hashlib
import binascii


SALT_STR = 'abcdefghijklmaopqrstuvwxyzABCDEFGHIJKLMAOPQRSTUVWXYZ12345678910'


def generate_password(password, hash_name: str='sha256', salt_length: int=8, iterations: int=1000) -> str:
    if not isinstance(password, bytes):
        password_byte = password.encode()
    else:
        password_byte = password

    salt_str = get_random_str(salt_length)
    salt_byte = salt_str.encode()

    iterations_str = str(iterations)

    hash_body = hashlib.pbkdf2_hmac(hash_name=hash_name, salt=salt_byte, iterations=iterations, password=password_byte)
    hash_str = binascii.hexlify(hash_body).decode()

    hash_password = '{}:{}:{}:{}'.format(hash_name, salt_str, hash_str, iterations_str)
    return hash_password


def verify_password(password, hash_password):
    if not isinstance(password, bytes):
        password_byte = password.encode()
    else:
        password_byte = password

    hash_name, salt, hash_pass, iterations_str = hash_password.split(':')
    salt_byte = salt.encode()
    iterations = int(iterations_str)
    user_password_byte = hashlib.pbkdf2_hmac(password=password_byte, hash_name=hash_name, salt=salt_byte, iterations=iterations)
    user_password = binascii.hexlify(user_password_byte).decode()
    if user_password == hash_pass:
        return True
    else:
        return False


def get_random_str(length: int):
    __random = ''.join(random.sample(SALT_STR, length))
    return __random
