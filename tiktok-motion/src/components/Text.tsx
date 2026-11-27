import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {FONT} from '../theme';

// Kata demi kata muncul dengan pegas. Kata diapit *bintang* diberi sorotan stabilo.
export const PopWords: React.FC<{
  text: string;
  delay?: number;
  size?: number;
  color?: string;
  highlight?: string;
  stagger?: number;
  align?: 'center' | 'left';
}> = ({text, delay = 0, size = 96, color = '#fff', highlight = '#14b8a6', stagger = 3, align = 'center'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = text.split(' ');
  return (
    <div style={{fontFamily: FONT, fontSize: size, fontWeight: 800, lineHeight: 1.12, letterSpacing: -size * 0.025, color, textAlign: align, display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', gap: `0 ${size * 0.26}px`}}>
      {words.map((w, i) => {
        const hl = w.startsWith('*');
        const clean = w.replace(/\*/g, '');
        const s = spring({frame: frame - delay - i * stagger, fps, config: {damping: 12, stiffness: 180, mass: 0.6}});
        const mark = interpolate(frame - delay - i * stagger, [6, 16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{display: 'inline-block', position: 'relative', transform: `translateY(${(1 - s) * 60}px) scale(${0.6 + s * 0.4})`, opacity: Math.min(1, s * 1.4)}}>
            {hl && (
              <span style={{position: 'absolute', left: -10, right: -10, bottom: '0.08em', height: '0.5em', background: highlight, borderRadius: 12, transform: `scaleX(${mark})`, transformOrigin: 'left', zIndex: 0, opacity: 0.9}} />
            )}
            <span style={{position: 'relative'}}>{clean}</span>
          </span>
        );
      })}
    </div>
  );
};

export const FadeOut: React.FC<{dur: number; children: React.ReactNode; out?: number}> = ({dur, children, out = 10}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [dur - out, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const s = interpolate(f, [dur - out, dur], [1, 1.06], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', inset: 0, opacity: o, transform: `scale(${s})`}}>{children}</div>;
};
