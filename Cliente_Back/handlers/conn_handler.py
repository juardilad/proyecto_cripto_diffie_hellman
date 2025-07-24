import socket
import threading
import json
import requests
from random import randint

class Connection:
    def __init__(self, host='127.0.0.1', port=8000, use_case=None):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.listen_thread = None
        self.use_case = use_case

    def connect(self):
        """Recibe un mensaje de conexión y establece el socket"""
        self.sock.connect((self.host, self.port))
        self.connected = True
        print(f"[Connection] Conectado a {self.host}:{self.port}")
        return self

    def send(self, direction, message, type):
        """Envía un mensaje al socket conectado"""
        if not self.connected:
            raise Exception("No hay conexión activa para enviar")

        payload = {
            "direction": direction,
            "message": message,
            "type": type,
        }

        try:
            self.sock.send(json.dumps(payload).encode('utf-8'))
            response = requests.post("http://localhost:5050/messages/encrypted", json=payload)
            print(f"[SEND] {payload}")
        except Exception as e:
            print(f"[Connection] Error al enviar: {e}")

    def listen(self):
        """Escucha mensajes del socket de forma bloqueante"""
        while self.connected:
            try:
                data = self.sock.recv(1024)
                if not data:
                    print("[Connection] Conexión cerrada por el servidor.")
                    self.connected = False
                    break

                decoded = data.decode('utf-8')
                payload = json.loads(decoded)

                direction = "recibido"
                message = payload.get("message")
                msg_type = payload.get("type")

                if msg_type == "generator":   
                    response = requests.post("http://localhost:5050/messages/encrypted", json=payload)
                    response = requests.post("http://localhost:5050/messages/decrypted", json=payload)
                    g, p, key_server = map(int, payload["message"].split(","))
                    a = randint(1, 100)
                    key_client = pow(g, a, p)
                    self.use_case.set_generator(g, p, a, key_client)
                    shared_key = pow(key_server, a, p)
                    self.use_case.set_key(shared_key)
                    direction = "enviado"
                    message = f"{key_client}"
                    type = "key"
                    payload2 = {
                        "direction": direction,
                        "message": message,
                        "type": type,
                    }
                    response = requests.post("http://localhost:5050/messages/encrypted", json=payload2)
                    response = requests.post("http://localhost:5050/messages/decrypted", json=payload2)
                    self.send(direction, message, type)
                    print(f"[RECV] {msg_type} - {direction}: {message}")

                else:
                    response = requests.post("http://localhost:5050/messages/encrypted", json=payload)
                    decrypted_message = self.use_case.decrypt_message(message)
                    payload2 = {
                        "direction": direction,
                        "message": decrypted_message,
                        "type": msg_type,
                    }
                    response = requests.post("http://localhost:5050/messages/decrypted", json=payload)

                    print(f"[RECV] {msg_type} - {direction}: {message}")
                    print(f"[RECV Desencriptado] {decrypted_message} - {direction}: {message}")

            except Exception as e:
                print(f"[Connection] Error al recibir: {e}")
                self.connected = False
                break

    def start_listening(self):
        """Lanza la escucha en un hilo separado"""
        if not self.listen_thread or not self.listen_thread.is_alive():
            self.listen_thread = threading.Thread(target=self.listen, daemon=True)
            self.listen_thread.start()
            print("[Connection] Escuchando en segundo plano...")

    def close(self):
        self.connected = False
        self.sock.close()
        print("[Connection] Conexión cerrada.")