from ecdsa import NIST256p
from ecdsa import SigningKey

################ ウォレット　
class Wallet(object):
    
    def __init__(self):
        ### 秘密鍵
        self._private_key = SigningKey.generate(curve=NIST256p)
        ### 公開鍵
        self._public_key = self.private_key.get_verifying_key()
        

if __name__ == '__main__':
    Wallet = Wallet()
    print(Wallet._public_key.toString.hex())