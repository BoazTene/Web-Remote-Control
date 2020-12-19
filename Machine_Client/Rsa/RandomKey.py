from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


class Key:
    def __init__(self):
        self.key = RSA.generate(2048)

        self.private = self.key.export_key()

        self.public = self.key.publickey().export_key()


key = Key()
data = "I met aliens in UFO. Here is the map.".encode("utf-8")

recipient_key = RSA.import_key(key.public)
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)

result = []

[ result.append(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]


print(result)