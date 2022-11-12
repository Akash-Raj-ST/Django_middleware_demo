# uvicorn main:app --reload
#running on http://127.0.0.1:8000

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast
import json



from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import simplejson as json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Data(BaseModel):
    public_key: str
    plain_text: str

@app.post("/encrypt/")
async def root(data: Data):
    public_key = data.public_key.encode()
    plain_text = data.plain_text.encode()

    encryptor = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted = encryptor.encrypt(plain_text)
   
    return {'result': str(encrypted)}
