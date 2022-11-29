import ecdsa
from ecdsa import SigningKey, VerifyingKey,NIST384p
import codecs
import pickle

#NOTE: Don't change publickey, or else you will isolate yourself from the rest of the protocol

f = open('pk','rb')

sk = SigningKey.from_der(pickle.load(f))
f.close()

f = open('publickey','rb')
vk = VerifyingKey.from_der(pickle.load(f))
f.close()
sig = sk.sign(b"message")
res = vk.verify(sig, b"message") # True
print(res)