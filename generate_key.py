import ecdsa
import pickle
import codecs

# SECP256k1 is the Bitcoin elliptic curve
sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
vk = sk.get_verifying_key()

#DO NOT UNCOMMENT
# with codecs.open('publickey', 'wb') as f:
#     #print(str(sk.to_string()))
#     pickle.dump((vk.to_der()),f)

with codecs.open('pk', 'wb') as f:
    #print(str(sk.to_string()))
    pickle.dump((sk.to_der()),f)