from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

import base64

def rsakeys():

    '''
        generate a pair of {private_key, public_key}
        output: unique set of {private_key, public_key} on each function call
    ''' 

    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey.export_key().decode(), publickey.export_key().decode()

def decrypt(pri,ciphertext):

    '''
        using the parameters pri->private_key,and ciphertext,
        the ciphertext is decrypted and returns it as string object
    '''

    ciphertext = base64.b64decode(ciphertext)

    key = RSA.importKey(pri)

    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15


    cipher = PKCS1_v1_5.new(key)
    message = cipher.decrypt(ciphertext,sentinel)

    return str(message.decode())