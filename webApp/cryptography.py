#RSA implementation

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast

#to store in DB
def rsakeys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey.export_key(), publickey.export_key()


def encrypt(rsa_publickey,plain_text):
    encryptor = PKCS1_OAEP.new(RSA.import_key(rsa_publickey))
    encrypted = encryptor.encrypt(plain_text.encode())
    return encrypted

def decrypt(rsa_privatekey, cipher):
    decryptor = PKCS1_OAEP.new(RSA.import_key(rsa_privatekey))
    decrypted = decryptor.decrypt(ast.literal_eval(str(cipher)))
    return decrypted
