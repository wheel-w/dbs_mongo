import base64
import hashlib
import logging

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logger = logging.getLogger("mongo")


class AESCipher:
    """
    AES-256加解密器 ECB模式
    """

    def __init__(self, key):
        self.key = hashlib.md5(key.encode("utf8")).hexdigest().encode("utf-8")  # md5之后刚好32字节
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)
        self.BLOCK_SIZE = 32  # Bytes

    def encrypt(self, plain_text):
        """
        加密
        :param plain_text: 需要加密的内容
        :return: cipher_text 已加密的内容
        """
        # 将需要加密的内容进行对齐操作
        pad_text = pad(plain_text.encode("utf-8"), self.BLOCK_SIZE)
        # 对齐后的bytes加密
        try:
            cipher_text = self.cipher_obj.encrypt(pad_text)
        except ValueError as err:
            logger.error(f"encrypt error: {err}")
            raise Exception(f"encrypt error: {err}")
        else:
            # AES加密时候得到的字符串不一定属于ASCII字符集，输出到终端或者保存时候可能存在问题，故此处再次使用base64编码
            return base64.b64encode(cipher_text).decode("utf-8")

    def decrypt(self, cipher_text):
        """
        解密
        :param cipher_text: 需要解密的内容
        :return: plain_text 已解密的内容
        """
        cipher_text = base64.b64decode(cipher_text.encode("utf-8"))
        try:
            pad_text = self.cipher_obj.decrypt(cipher_text)
        except ValueError as err:
            logger.error(f"decrypt error: {err}")
            raise Exception(f"decrypt error: {err}")

        try:
            plain_text = unpad(pad_text, self.BLOCK_SIZE).decode("utf-8")
        except ValueError:
            logger.error(f"unpad error, the padding is incorrect.cipher_text={cipher_text}, pad_text={pad_text}")
            raise Exception("密码解析错误")
        else:
            return plain_text


secret_key = "this is secret"
aes_cipher = AESCipher(secret_key)
