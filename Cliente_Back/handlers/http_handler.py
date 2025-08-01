from flask import Flask, request, jsonify
from flask_cors import CORS
from models.message import Message
from models.memory import Memory 
from random import randint
import requests

def create_http_handler(use_case, conn_handler=None):
    app = Flask(__name__)
    CORS(app)

    @app.route('/messages/send', methods=['POST'])
    def send_message():
        data = request.json
        try:
            message = data.get('message')
            type = data.get('type')
            encrypted_message = use_case.encrypt_message(message)
            use_case.add_decrypted_message("enviado", message, "generator")
            conn_handler.send(encrypted_message, type)
            return jsonify({"status": "success"}), 201
        except Exception as e:
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