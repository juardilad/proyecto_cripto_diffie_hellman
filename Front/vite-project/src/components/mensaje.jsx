import React from 'react';

const Mensaje = ({data}) => {
  return (
    <div className="mensaje">
        <p>Direccion: {data.direction}, Mensaje: {data.message}, Tipo: {data.type}</p>
    </div>
  )
}

export default Mensaje