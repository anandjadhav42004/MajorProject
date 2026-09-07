import React from 'react';

function Stat({ t, v, s }) {
  return (
    <div className="stat">
      <span>{t}</span>
      <strong>{v}</strong>
      <small>{s}</small>
    </div>
  );
}

export default Stat;
