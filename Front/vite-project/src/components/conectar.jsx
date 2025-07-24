import React from 'react';
import { useNavigate } from 'react-router-dom';

const Conectar = () => {
  const navigate = useNavigate();

  const conectar = async () => {
    console.log("Intentando conectar...");

    try {
      const response = await fetch('http://localhost:5000/connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Conectado:", data);
        navigate('/general');
      } else {
        console.error("Error en conexión:", data.error);
        alert(`Error al conectar: ${data.error}`);
      }
    } catch (err) {
      console.error("Fallo al hacer la petición:", err);
      alert("No se pudo conectar al servidor.");
    }
  };

  return (
    <button type='button' className="conectar" onClick={conectar}>
      Conectar
    </button>
  );
};

export default Conectar;
