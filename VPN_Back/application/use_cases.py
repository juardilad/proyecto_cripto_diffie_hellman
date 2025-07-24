from models.generator import Generator
from models.memory import Memory
from utils.cipher_system import AESCipher
import base64

class UseCase:

    def __init__(self, memory: Memory):
        self.memory = memory
        self.generator = Generator(g=0, p=0, a=0, A=0)

    def add_encrypted_message(self, direction: str, message: str, type: str):
        self.memory.add_encrypted_message(direction, message, type)

    def add_decrypted_message(self, direction: str, message: str, type: str):
        self.memory.add_decrypted_message(direction, message, type)

    def get_encrypted_messages(self):
        return self.memory.get_encrypted_messages()
    
    def get_last_encrypted_message(self):
        messages = self.memory.get_encrypted_messages()
        return messages[-1] if messages else None
    
    def get_last_decrypted_message(self):
        messages = self.memory.get_decrypted_messages()
        return messages[-1] if messages else None

    def get_decrypted_messages(self):
        return self.memory.get_decrypted_messages()

    def clear_messages(self):
        self.memory.clear_messages()

    def get_generator(self):
        return self.memory.get_generator()

    def set_generator(self, g: int, p: int, a: int, A: int):
        self.memory.set_generator(g, p, a, A)

    def set_key(self, B: int):
        self.memory.set_key_B(B)

    def get_key_B(self):
        return self.memory.get_key_B()

    def decrypt_message(self, ciphertext: bytes) -> str:
        key = self.memory.get_key_B()
        aes_cipher = AESCipher(key.to_bytes(16, 'big'))
        return aes_cipher.decrypt(ciphertext)


    def encrypt_message(self, plaintext: str) -> bytes:
        key = self.memory.get_key_B()
        aes_cipher = AESCipher(key.to_bytes(16, 'big'))
        return aes_cipher.encrypt(plaintext)