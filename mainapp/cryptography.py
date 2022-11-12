#RSA implementation

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast
import json

#to store in DB
def rsakeys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey.export_key().decode(), publickey.export_key().decode()


def encrypt(rsa_publickey,plain_text):
    encryptor = PKCS1_OAEP.new(RSA.import_key(rsa_publickey))
    encrypted = encryptor.encrypt(plain_text.encode())
    return encrypted

def decrypt(rsa_privatekey, cipher):
    print(cipher)
    decryptor = PKCS1_OAEP.new(RSA.import_key(rsa_privatekey.encode()))
    decrypted = decryptor.decrypt(ast.literal_eval(str(cipher)))
    print('done',decrypted)
    return decrypted


# text = "hello"
# pri,pub = rsakeys()
# # print(pub.decode())
# cipher = encrypt(pub,text)
# print(type(cipher))

# decrypt_text = decrypt(pri,cipher)
# print(decrypt_text)

