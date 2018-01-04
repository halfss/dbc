#coding=utf8
import binascii
import hashlib
from ecdsa import SigningKey, VerifyingKey, NIST384p
import base58

version = '00'

def get_addr(publick_hex):
    public_key_str = binascii.unhexlify(publick_hex)
    psha256 = sha256(public_key_str)
    pripemd160 = ripemd160(psha256)
    after_version = "%s%s" % (version, pripemd160)
    psha2561 = sha256(after_version)
    psha2562 = sha256(psha2561)
    after_check =  "%s%s" % (psha2562[:8], after_version)
    addr = base58.b58encode_check(after_check)
    return addr[:34]

def gen_private_key(seed = ''):
    if seed:
        sk = SigningKey.from_string(seed, curve=NIST384p)
    else:
        sk = SigningKey.generate(curve=NIST384p)
    return binascii.hexlify(sk.to_string())

def get_public_key(private_key_hex):
    pk_string = binascii.unhexlify(private_key_hex)
    sk = SigningKey.from_string(pk_string, curve = NIST384p)
    publick = sk.get_verifying_key()
    print publick.to_string()
    return binascii.hexlify(publick.to_string())

def sign(private_key_hex, seed):
    pk_string = binascii.unhexlify(private_key_hex)
    sk = SigningKey.from_string(pk_string, curve = NIST384p)
    signature = sk.sign(seed)
    return binascii.hexlify(signature)

def verify(sign_hex, publick_hex, message):
    signature = binascii.unhexlify(sign_hex)
    vk_str = binascii.unhexlify(publick_hex)
    vk = VerifyingKey.from_string(vk_str, curve=NIST384p)
    return vk.verify(signature, message)


def sha256(s):
    m = hashlib.sha256()
    m.update(s)
    return m.hexdigest()


def ripemd160(s):
    h = hashlib.new('ripemd160')
    h.update(b"%s" % s)
    return h.hexdigest()

if __name__ == "__main__":
    pk_hex = gen_private_key()
    publick_hex = get_public_key(pk_hex)
    addr = get_addr(publick_hex)
    print pk_hex
    print publick_hex
    print addr
    signout_hex = sign(pk_hex, "asdfasfee")
    print verify(signout_hex, publick_hex, "asdfasfee")
    signout_hex = sign("32097224adacfa5cadf7eb7994037ecea41d3db3cce35ae4eea01e13868c75dbef378da43d0839f24dba21a79afaed47", "d7fced03e7fcef568361da142390dd85866a673573569f75c4c6dd565dde0fe3")
    print signout_hex
