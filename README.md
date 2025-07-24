# Proyecto Educativo: Criptografía con Diffie-Hellman y AES

Este proyecto fue desarrollado con fines meramente educativos, con el objetivo de comprender e ilustrar los conceptos fundamentales de la criptografía moderna, incluyendo el intercambio de claves Diffie-Hellman, el cifrado simétrico AES, y la transmisión de mensajes a través de sockets TCP/IP.

Tanto el código como el diseño del sistema están orientados a facilitar el aprendizaje y la experimentación, y no deben considerarse seguros para entornos de producción.

## 🧠 Conceptos aplicados

- Intercambio de claves Diffie-Hellman
- Cifrado y descifrado de mensajes con AES (modo CBC)
- Serialización y transmisión de datos con sockets TCP
- Interacción cliente-servidor en Python
- Comunicación básica Flask para APIs HTTP
- Envío y recepción de mensajes cifrados

## 🚀 ¿Qué hace este proyecto?

- Un cliente y un servidor intercambian claves mediante Diffie-Hellman.
- A partir de la clave compartida, ambos generan una clave AES simétrica.
- Se establece una conexión segura para enviar mensajes cifrados entre cliente y servidor.
- Se proporciona una interfaz básica HTTP en Flask para simular la comunicación.
- Los mensajes son cifrados antes de enviarse y descifrados al recibirlos.

## 🛠️ Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/juardilad/proyecto_cripto_diffie_hellman.git
cd proyecto_cripto_diffie_hellman
```
2. Instalar dependencias:
```bash
cd Cliente_Back
pip install -r requirements.txt
```

```bash
cd VPN_Back
pip install -r requirements.txt
```

```bash
cd Front/vite-project
npm install
```
3. Correr el servidor de manera local:

```bash
cd VPN_Back
python main.py
```

4. Correr el punto cliente:
   
```bash
cd Cliente_Back
python main.py
```

5. Acceder a la interfaz gráfica para evidenciar resultados:

```bash
cd Front/vite-project
npm run dev
```

Acceder a: `http:localhost:5173`

## 📚 Notas educativas

No se utiliza autenticación ni integridad en los mensajes.

Este proyecto está diseñado como una herramienta para comprender cómo funcionan los principios criptográficos a bajo nivel, y fomentar la curiosidad sobre seguridad de la información.
