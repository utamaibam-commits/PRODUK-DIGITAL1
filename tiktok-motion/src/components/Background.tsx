import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {C} from '../theme';

// Latar gradasi emerald yang "bernapas" + titik grid halus.
export const Background: React.FC<{tint?: string}> = ({tint = C.brand2}) => {
  const f = useCurrentFrame();
  const x1 = 30 + Math.sin(f / 60) * 12;
  const y1 = 20 + Math.cos(f / 75) * 8;
  const x2 = 75 + Math.cos(f / 50) * 10;
  const y2 = 80 + Math.sin(f / 70) * 8;
  const rot = interpolate(f, [0, 900], [0, 25]);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(60% 40% at ${x1}% ${y1}%, ${tint}55 0%, transparent 70%),
          radial-gradient(55% 35% at ${x2}% ${y2}%, #6366f140 0%, transparent 70%),
          linear-gradient(160deg, ${C.bg2} 0%, ${C.bg} 60%, #020f0d 100%)`,
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage:
            'radial-gradient(rgba(255,255,255,0.09) 1.6px, transparent 1.6px)',
          backgroundSize: '44px 44px',
          transform: `rotate(${rot}deg) scale(1.6)`,
          opacity: 0.55,
          maskImage: 'radial-gradient(70% 60% at 50% 50%, black, transparent)',
          WebkitMaskImage:
            'radial-gradient(70% 60% at 50% 50%, black, transparent)',
        }}
      />
    </AbsoluteFill>
  );
};
