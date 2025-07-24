import React from 'react';
import Mensaje from '../components/mensaje';

const MensajesTodos= ({mensajes}) => {
  return (
    <div className="mensajes-todos">
      {mensajes.map((msg, index) => (
        <Mensaje key={index} data={msg} />
      ))}
    </div>
  )
}

export default MensajesTodos