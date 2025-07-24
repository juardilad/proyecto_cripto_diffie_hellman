import React from 'react';

const Mensaje = ({data}) => {
  return (
    <div className="mensaje">
        <p className='mensaje'>Direccion: {data.direction}, Mensaje: {data.message}, Tipo: {data.type}</p>
    </div>
  )
}

export default Mensaje