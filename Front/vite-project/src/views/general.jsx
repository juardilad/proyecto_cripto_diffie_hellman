import React, { useEffect, useState } from 'react';
import Mensaje from '../components/mensaje';
import MensajesTodos from '../components/mensajes_todos';

const General = () => {
  const [mensajeServidor, setMensajeServidor] = useState('');
  const [mensajeCliente, setMensajeCliente] = useState('');

  const [mensajesServidorCifrados, setMensajesServidorCifrados] = useState([]);
  const [mensajesServidorDescifrados, setMensajesServidorDescifrados] = useState([]);
  const [mensajesClienteCifrados, setMensajesClienteCifrados] = useState([]);
  const [mensajesClienteDescifrados, setMensajesClienteDescifrados] = useState([]);

  // 🔁 Función para obtener mensajes de todos los puertos
  const fetchMensajes = async () => {
    try {
      const [encS, decS, encC, decC] = await Promise.all([
        fetch('http://localhost:5000/messages/encrypted'),
        fetch('http://localhost:5000/messages/decrypted'),
        fetch('http://localhost:5050/messages/encrypted'),
        fetch('http://localhost:5050/messages/decrypted'),
      ]);

      const dataEncS = await encS.json();
      const dataDecS = await decS.json();
      const dataEncC = await encC.json();
      const dataDecC = await decC.json();

      setMensajesServidorCifrados(dataEncS);
      setMensajesServidorDescifrados(dataDecS);
      setMensajesClienteCifrados(dataEncC);
      setMensajesClienteDescifrados(dataDecC);
    } catch (error) {
      console.error("Error al obtener mensajes:", error);
    }
  };

  // ⏱️ Loop infinito: cada 1 segundo
  useEffect(() => {
    fetchMensajes(); // primero una vez
    const interval = setInterval(fetchMensajes, 1000); // luego cada 1s
    return () => clearInterval(interval); // limpiar en desmontaje
  }, []);

  const enviarServidor = async (e) => {
    e.preventDefault();
    if (!mensajeServidor.trim()) return;

    try {
      await fetch('http://localhost:5000/messages/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: mensajeServidor, type: 'text' }),
      });
      setMensajeServidor('');
    } catch (err) {
      console.error('Error al enviar desde servidor:', err);
    }
  };

  const enviarCliente = async (e) => {
    e.preventDefault();
    if (!mensajeCliente.trim()) return;

    try {
      await fetch('http://localhost:5050/messages/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: mensajeCliente, type: 'text' }),
      });
      setMensajeCliente('');
    } catch (err) {
      console.error('Error al enviar desde cliente:', err);
    }
  };

  return (
    <div className="pantalla-general">
      {/* SERVIDOR */}
      <div className='columna_sujeto'>
        <h2>Servidor</h2>
        <form onSubmit={enviarServidor}>
          <input
            type="text"
            value={mensajeServidor}
            onChange={(e) => setMensajeServidor(e.target.value)}
            placeholder="Escribe un mensaje..."
          />
          <button type="submit">Enviar</button>
        </form>

        <h4>Mensajes cifrados</h4>
        <MensajesTodos mensajes={mensajesServidorCifrados} />

        <h4>Mensajes descifrados</h4>
        <MensajesTodos mensajes={mensajesServidorDescifrados} />
      </div>

      {/* CLIENTE */}
      <div className="columna_sujeto">
        <h2>Cliente</h2>
        <form onSubmit={enviarCliente}>
          <input
            type="text"
            value={mensajeCliente}
            onChange={(e) => setMensajeCliente(e.target.value)}
            placeholder="Escribe un mensaje..."
          />
          <button type="submit">Enviar</button>
        </form>

        <h4>Mensajes cifrados</h4>
         <MensajesTodos mensajes={mensajesClienteCifrados} />

        <h4>Mensajes descifrados</h4>
        <MensajesTodos mensajes={mensajesClienteDescifrados} />
      </div>
    </div>
  );
};

export default General;
