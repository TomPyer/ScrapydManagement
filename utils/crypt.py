#! coding:utf-8
import binascii
import random
import hashlib
from pyDes import *
from rsa import sign, encrypt, decrypt


def des_encrypt(data=None, key=None):
    '''des加密数据
    '''
    if not data: return data
    try:
        if not key:
            key = 'tangxl'
        k = des(str(key[0:8]), CBC, str(key[0:8]), pad=None, padmode=PAD_PKCS5)
        res = binascii.b2a_hex(k.encrypt(str(data).encode('GBK')))
        return res
    except Exception as ce:
        print(ce)
        return data


def des_decrypt(data=None, key=None):
    '''解密数据
    '''
    if not data: return data
    try:
        if not key:
            key = 'tangxl'
        k = des(str(key[0:8]), CBC, str(key[0:8]), pad=None, padmode=PAD_PKCS5)
        d = k.decrypt(binascii.a2b_hex(str(data)))
        return d.decode('GBK')
    except Exception as ce:
        print(ce)
        return data


def gen_md5_salt():
    '''生成MD5的盐值
    '''
    abc = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(abc))

    return "".join(chars)


def md5_encrypt(password, salt=None):
    '''md5加密
    '''
    return hashlib.md5(password + salt).hexdigest()


def rsa_encrypt(data, pub_key):
    try:
        return binascii.b2a_hex(encrypt(data, pub_key))
    except:
        return data


def rsa_decrypt(data, pri_key):
    try:
        return decrypt(binascii.a2b_hex(data), pri_key)
    except:
        return data


def signature(data, pri_key):
    try:
        return binascii.b2a_hex(sign(data, pri_key, 'SHA-1'))
    except:
        return data
