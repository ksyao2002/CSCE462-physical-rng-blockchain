import ecdsa
import pickle

# SECP256k1 is the Bitcoin elliptic curve
sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
vk = sk.get_verifying_key()
print(vk.to_string())



with open('.pk', 'wb') as pkfile:
    pickle.dump(sk, pkfile)