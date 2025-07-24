from models.message import Message
from models.generator import Generator
from models.key import Key

class Memory:

    def __init__(self):
        self.encrypted_messages = []
        self.decrypted_messages = []
        self.generator = Generator(g=0, p=0, a=0, A=0)
        self.key = Key(B=0)

    def add_encrypted_message(self, direction: str, message: str, type: str):
        new_message = Message(direction=direction, message=message, type=type)
        self.encrypted_messages.append(new_message)

    def get_encrypted_messages(self):
        return self.encrypted_messages

    def add_decrypted_message(self, direction: str, message: str, type: str):
        new_message = Message(direction=direction, message=message, type=type)
        self.decrypted_messages.append(new_message)

    def get_decrypted_messages(self):
        return self.decrypted_messages

    def clear_messages(self):
        self.encrypted_messages.clear()
        self.decrypted_messages.clear()

    def set_generator(self, g: int, p: int, a: int, A: int):
        self.generator.g = g
        self.generator.p = p
        self.generator.a = a
        self.generator.A = A

    def set_key_B(self, B:int):
        self.key.B = B

    def get_key_B(self):
        return self.key.B

    def get_generator(self):
        return self.generator