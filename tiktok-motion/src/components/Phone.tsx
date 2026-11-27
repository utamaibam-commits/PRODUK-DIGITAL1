import React from 'react';
import {C} from '../theme';

// Bingkai iPhone/Android generik (tanpa logo merek) berukuran 600x1230 px.
export const PHONE_W = 600;
export const PHONE_H = 1230;

export const Phone: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div
    style={{
      width: PHONE_W,
      height: PHONE_H,
      borderRadius: 86,
      padding: 16,
      background: 'linear-gradient(145deg,#2b3a37,#0b1311 40%,#1d2a27)',
      boxShadow:
        '0 0 0 3px #3d4f4b inset, 0 60px 120px -30px rgba(0,0,0,.75), 0 0 80px -10px rgba(20,184,166,.35)',
      position: 'relative',
      ...style,
    }}
  >
    <div
      style={{
        width: '100%',
        height: '100%',
        borderRadius: 72,
        overflow: 'hidden',
        background: C.appBg,
        position: 'relative',
      }}
    >
      {children}
      {/* dynamic island / kamera */}
      <div
        style={{
          position: 'absolute',
          top: 22,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 150,
          height: 42,
          borderRadius: 30,
          background: '#050807',
          zIndex: 50,
        }}
      />
    </div>
  </div>
);
