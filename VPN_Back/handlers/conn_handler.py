import socket
import threading
import json
import requests

class Connection:
    def __init__(self, host='0.0.0.0', port=8000, use_case=None):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.listen_thread = None
        self.use_case = use_case

    def connect(self):
        """Recibe un mensaje de conexión y establece el socket"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.connected = True
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print(f"[Connection] Conectado a {self.host}:{self.port}")
        return self

    def send(self, message, type):
        """Envía un mensaje al socket conectado"""
        if not self.connected:
            raise Exception("No hay conexión activa para enviar")

        payload_send = {
            "direction": "enviado",
            "message": message,
            "type": type,
        }
        
        if not self.conn:
            raise Exception("No hay conexión activa con el cliente")

        try:
            self.conn.send(json.dumps(payload_send).encode('utf-8'))
            response = requests.post("http://localhost:5000/messages/encrypted", json=payload_send)
            print(f"[SEND] {payload_send}")
        except Exception as e:
            print(f"[Connection] Error al enviar: {e}")
            raise


    def listen(self):
        """Escucha mensajes del socket de forma bloqueante"""
        while self.connected:
            try:
                data = self.conn.recv(1024)
                if not data:
                    print("[Connection] Conexión cerrada por el servidor.")
                    self.connected = False
                    break

                decoded = data.decode('utf-8')
                payload_received = json.loads(decoded)

                direction = "recibido"
                message = payload_received.get("message")
                msg_type = payload_received.get("type")
                payload_received["direction"] = direction

                if str(msg_type) == "key":
                    response = requests.post("http://localhost:5000/messages/encrypted", json=payload_received)
                    response = requests.post("http://localhost:5000/messages/decrypted", json=payload_received)
                    generator = self.use_case.get_generator()
                    B = int(payload_received["message"])  # <- La clave pública del cliente
                    shared_key = pow(B, generator.a, generator.p)
                    self.use_case.set_key(shared_key)
                    print(f"[RECV] {msg_type} - {direction}: {message}")
                else:
                    response = requests.post("http://localhost:5000/messages/encrypted", json=payload_received)
                    decrypted_message = self.use_case.decrypt_message(message)
                    payload2 = {
                        "direction": "enviado",
                        "message": decrypted_message,
                        "type": msg_type,
                    }
                    response = requests.post("http://localhost:5000/messages/decrypted", json=payload2)

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