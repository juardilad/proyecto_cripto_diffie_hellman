import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers.http_handler import create_http_handler
from handlers.conn_handler import Connection
from application.use_cases import UseCase
from models.memory import Memory

if __name__ == "__main__":
    # 1. Crear instancias
    memory = Memory()
    use_case = UseCase(memory)
    conn_handler = Connection(host='127.0.0.1', port=8000, use_case=use_case)

    # 2. Conectar y lanzar escucha en un hilo separado
    conn = conn_handler.connect()       
    conn_handler.start_listening()   # Espera una conexión entrante (bloqueante hasta que alguien se conecte)

    # 3. Crear la app HTTP y lanzarla
    app = create_http_handler(use_case, conn)
    app.run(port=5050, debug=True, use_reloader=False)

