import hashlib
from Crypto.Cipher import AES
from Crypto import Random


class Crypto:
    def __init__(self, password):
        self.__dk = self.__derive_key(password)

    @staticmethod
    def __derive_key(password):
        """
        derives cryptographic key using pbkdf2 key derivation scheme
        salt = sha3_256 digest of password string, 16 bytes as recommended
        """
        salt = hashlib.sha3_256(password.encode()).digest()
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.__dk, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.__dk, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    @staticmethod
    def _pad(s, bs=32):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
