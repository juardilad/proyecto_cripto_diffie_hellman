from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class AESCipher:
    def __init__(self, key: bytes):
        # Asegurarse que la clave tenga 16, 24 o 32 bytes (AES-128, AES-192, AES-256)
        self.key = key.ljust(16, b'0')[:16]  # Rellenar o cortar a 16 bytes si es necesario

    def encrypt(self, plaintext: str) -> str:
        """
        Cifra el mensaje de texto plano.
        Retorna una cadena codificada en base64 que contiene IV + mensaje cifrado.
        """
        msg = plaintext.encode('utf-8')
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        enc_msg = cipher.encrypt(pad(msg, 16))
        payload = iv + enc_msg  # Concatenamos IV + mensaje
        return base64.b64encode(payload).decode('utf-8')  # Codificamos en base64 para transporte

    def decrypt(self, encoded_payload: str) -> str:
        """
        Descifra una cadena base64 que contiene IV + mensaje cifrado.
        Retorna el texto plano original como string.
        """
        try:
            payload = base64.b64decode(encoded_payload)
            iv = payload[:16]
            enc_msg = payload[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
            msg = unpad(cipher.decrypt(enc_msg), 16)
            return msg.decode('utf-8')
        except Exception as e:
            print(f"[AESCipher] Error al descifrar: {e}")
            return None
