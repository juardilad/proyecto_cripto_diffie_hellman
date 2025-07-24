from flask import Flask, request, jsonify
from flask_cors import CORS
from models.message import Message
from models.memory import Memory 
import requests
from random import randint

def create_http_handler(use_case, conn_handler=None):
    app = Flask(__name__)
    CORS(app)

    @app.route('/connection', methods=['POST'])
    def create_connection():
        if not conn_handler.connected:
            return jsonify({"error": "El cliente no está conectado al socket"}), 400

        try:
            p = 214748364
            g = 6
            a = randint(1, 100)
            A = pow(g, a, p )
            use_case.set_generator(g, p, a, A)
            message = f"{g},{p},{A}"
            use_case.add_decrypted_message("enviado", message, "generator")
            conn_handler.send(message, "generator")
            return jsonify({"status": "generator enviado"}), 200

        except Exception as e:
            print(f"[ERROR /connection]: {e}")
            return jsonify({"error": str(e)}), 400
        

    @app.route('/messages/send', methods=['POST'])
    def send_message():
        data = request.json
        print("[POST /messages/send] Payload recibido:", data)
        try:
            direction = "enviado"
            message = data.get('message')
            type = data.get('type')
            encrypted_message = use_case.encrypt_message(message)
            use_case.add_decrypted_message(direction, message, type)
            use_case.add_encrypted_message(direction, encrypted_message, type)
            conn_handler.send(encrypted_message, type)
            return jsonify({"status": "success"}), 201
        except Exception as e:
            print("[ERROR /messages/send]:", str(e))
            return jsonify({"error": str(e)}), 400

    @app.route('/messages/encrypted', methods=['POST'])
    def add_encrypted_message():
        data = request.json
        try:
            direction = data.get('direction')
            message = data.get('message')
            type = data.get('type')
            use_case.add_encrypted_message(direction, message, type)
            return jsonify({"status": "success"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/messages/decrypted', methods=['POST'])
    def add_decrypted_message():
        data = request.json
        try:
            direction = data.get('direction')
            message = data.get('message')
            type = data.get('type')
            use_case.add_decrypted_message(direction, message, type)
            return jsonify({"status": "success"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route('/messages/encrypted', methods=['GET'])
    def get_encrypted_messages():
        try:
            messages = use_case.get_encrypted_messages()
            return jsonify([{"direction": msg.direction, "message": msg.message, "type": msg.type} for msg in messages]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/messages/decrypted', methods=['GET'])
    def get_decrypted_messages():   
        try:
            messages = use_case.get_decrypted_messages()
            return jsonify([{"direction": msg.direction, "message": msg.message, "type": msg.type} for msg in messages]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app  