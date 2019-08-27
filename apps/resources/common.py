from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
from django.conf import settings
import random
import string


def encrypt_string(string: str) -> str:
    '''
    加密字符串
    :param string: 需加密字符串
    :return: 加密字符串
    '''
    iv = Random.new().read(AES.block_size)
    myclipher = AES.new(settings.ENCRYPT_KEY, AES.MODE_CFB, iv)
    clipher_text = iv + myclipher.encrypt(string.encode('utf-8'))

    return b2a_hex(clipher_text).decode()


def decrypt_string(encrypt_string: str) -> str:
    '''
    字符串解密
    :param encrypt_string: 密文
    :return: 解密后字符串
    '''
    # key = settings.ENCRYPT_KEY
    # string = encrypt_string.encode('utf-8')
    # print(string[16:])

    mydecypt = AES.new(settings.ENCRYPT_KEY, AES.MODE_CFB, a2b_hex(encrypt_string)[:16])
    descrypttext = mydecypt.decrypt(a2b_hex(encrypt_string)[16:])

    return descrypttext.decode()


def generate_username(length: int) -> str:
    letters = string.ascii_letters + string.digits
    username = ''
    for i in range(length):
        username += random.choice(letters)
    return username


def generate_password(length: int) -> str:
    letters = string.ascii_letters + string.digits
    password = ''
    for i in range(length):
        password += random.choice(letters)
    return password
