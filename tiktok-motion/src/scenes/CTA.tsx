import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Background} from '../components/Background';
import {IcArrowUp, IcChart} from '../components/Icons';
import {C, FONT} from '../theme';

export type CTAProps = {
  readonly price: string;
  readonly lynkUrl: string;
};

export const CTA: React.FC<CTAProps> = ({price, lynkUrl}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const logo = spring({frame: f, fps, config: {damping: 12}});
  const tag = spring({frame: f - 12, fps, config: {damping: 8, stiffness: 140}});
  const btn = spring({frame: f - 26, fps, config: {damping: 12}});
  const bob = Math.sin(f / 5) * 18;
  const glow = 0.5 + Math.sin(f / 6) * 0.5;
  const sweep = interpolate(f % 45, [0, 45], [-120, 220]);
  return (
    <AbsoluteFill>
      <Background tint={C.brand2} />
      <AbsoluteFill style={{fontFamily: FONT, color: '#fff', alignItems: 'center', padding: '170px 80px 0'}}>
        {/* panah ke bio (TikTok menaruh link di profil, di atas) */}
        <div style={{transform: `translateY(${bob}px) scale(${btn})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
          <div style={{width: 150, height: 150, borderRadius: 75, background: C.mint, display: 'grid', placeItems: 'center', boxShadow: `0 0 ${40 + glow * 50}px ${C.mint}`}}>
            <IcArrowUp size={96} color={C.bg} stroke={3} />
          </div>
        </div>
        <div style={{fontSize: 120, fontWeight: 800, letterSpacing: -3, marginTop: 40, transform: `scale(${btn})`}}>Link di bio</div>
        <div style={{display: 'flex', alignItems: 'center', gap: 24, marginTop: 80, transform: `scale(${logo})`}}>
          <div style={{width: 120, height: 120, borderRadius: 36, background: `linear-gradient(135deg,${C.brand},${C.brand2})`, display: 'grid', placeItems: 'center', boxShadow: `0 20px 40px -14px ${C.brand2}`}}><IcChart size={70} /></div>
          <div>
            <div style={{fontSize: 96, fontWeight: 800, lineHeight: 1}}>KasRapi</div>
            <div style={{fontSize: 38, fontWeight: 700, color: C.soft}}>Buku Kas, Stok & Laba UMKM</div>
          </div>
        </div>
        <div style={{marginTop: 70, position: 'relative', overflow: 'hidden', padding: '30px 64px', borderRadius: 40, background: '#fff', color: C.bg, transform: `scale(${tag}) rotate(${(1 - tag) * 12 - 2}deg)`, boxShadow: '0 30px 60px -20px rgba(0,0,0,.6)'}}>
          <div style={{fontSize: 40, fontWeight: 700, color: C.ink2, textAlign: 'center'}}>Sekali bayar</div>
          <div style={{fontSize: 150, fontWeight: 800, letterSpacing: -5, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>{price}</div>
          <div style={{position: 'absolute', top: 0, bottom: 0, left: `${sweep}%`, width: '30%', background: 'linear-gradient(90deg,transparent,rgba(20,184,166,.25),transparent)', transform: 'skewX(-20deg)'}} />
        </div>
        <div style={{marginTop: 60, fontSize: 48, fontWeight: 800, color: C.mint, opacity: btn}}>{lynkUrl}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
