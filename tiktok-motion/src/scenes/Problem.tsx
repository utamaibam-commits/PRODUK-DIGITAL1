import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Background} from '../components/Background';
import {FadeOut} from '../components/Text';
import {C, FONT, rp} from '../theme';

// Omzet terlihat besar, lalu "dicakar" satu per satu oleh potongan yang jarang dicatat.
const CUTS: {label: string; amount: number; color: string}[] = [
  {label: 'Admin & layanan Shopee', amount: 5400, color: C.orange},
  {label: 'Biaya per pesanan', amount: 1250, color: C.warn},
  {label: 'Modal barang (HPP)', amount: 24000, color: C.indigo},
];

export const Problem: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const start = 45000;
  const cutAt = (i: number) => 24 + i * 22;
  const done = CUTS.reduce((acc, c, i) => acc + c.amount * interpolate(f, [cutAt(i), cutAt(i) + 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), 0);
  const value = start - done;
  const head = spring({frame: f, fps, config: {damping: 16}});
  const finalIn = spring({frame: f - 96, fps, config: {damping: 11}});
  const dapur = spring({frame: f - 112, fps, config: {damping: 10}});
  const shake = f > cutAt(0) && f < cutAt(2) + 14 ? Math.sin(f * 2.3) * 5 : 0;
  return (
    <AbsoluteFill>
      <Background />
      <FadeOut dur={dur}>
        <AbsoluteFill style={{fontFamily: FONT, color: '#fff', padding: '230px 90px 0', alignItems: 'center'}}>
          <div style={{fontSize: 48, fontWeight: 700, opacity: head, color: C.soft}}>Jual 3 bungkus di Shopee</div>
          <div style={{fontSize: 150, fontWeight: 800, letterSpacing: -4, fontVariantNumeric: 'tabular-nums', margin: '18px 0 40px', transform: `translateX(${shake}px) scale(${0.8 + head * 0.2})`, color: f > cutAt(2) + 12 ? C.mint : '#fff'}}>
            {rp(value)}
          </div>
          <div style={{width: '100%', display: 'flex', flexDirection: 'column', gap: 22}}>
            {CUTS.map((c, i) => {
              const s = spring({frame: f - cutAt(i) + 8, fps, config: {damping: 13, stiffness: 170}});
              return (
                <div key={c.label} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '26px 34px', borderRadius: 32, background: 'rgba(255,255,255,.08)', border: `2px solid ${c.color}`, transform: `translateX(${(1 - s) * 700}px) rotate(${(1 - s) * 6}deg)`, opacity: s}}>
                  <span style={{fontSize: 40, fontWeight: 700}}>{c.label}</span>
                  <span style={{fontSize: 48, fontWeight: 800, color: C.neg, fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}}>-{rp(c.amount)}</span>
                </div>
              );
            })}
          </div>
          <div style={{marginTop: 54, fontSize: 64, fontWeight: 800, textAlign: 'center', transform: `scale(${finalIn})`, lineHeight: 1.15}}>
            Untung beneran cuma <span style={{color: C.mint}}>{rp(14350)}</span>
          </div>
          <div style={{marginTop: 34, fontSize: 46, fontWeight: 700, padding: '18px 34px', borderRadius: 99, background: C.neg, transform: `scale(${dapur}) rotate(-3deg)`}}>
            …itu pun kepakai belanja dapur 🍳
          </div>
        </AbsoluteFill>
      </FadeOut>
    </AbsoluteFill>
  );
};
