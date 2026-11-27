import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {AppHome, AppSaleSheet, BottomNav} from '../components/AppScreen';
import {Background} from '../components/Background';
import {IcChart} from '../components/Icons';
import {Phone, PHONE_H} from '../components/Phone';
import {FadeOut} from '../components/Text';
import {C, FONT} from '../theme';

// Adegan 3+4: HP muncul (perkenalan KasRapi), lalu demo Beranda dan Catat Penjualan.
const HOME_AT = 70; // layar splash berganti ke Beranda
const TAP_AT = 200; // jari mengetuk tombol +
const SHEET_AT = 210;

const Callout: React.FC<{text: string; at: number; top: number; side: 'left' | 'right'; color?: string}> = ({text, at, top, side, color = C.mint}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 12, stiffness: 150}});
  const out = interpolate(f, [at + 70, at + 80], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top, [side]: 40, maxWidth: 470, fontFamily: FONT, fontSize: 44, fontWeight: 800, lineHeight: 1.15, color: C.bg, background: color, padding: '22px 30px', borderRadius: 30, boxShadow: '0 24px 50px -20px rgba(0,0,0,.6)', transform: `scale(${s}) rotate(${side === 'left' ? -3 : 3}deg)`, opacity: Math.min(s, out), zIndex: 10}}>
      {text}
    </div>
  );
};

export const AppDemo: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rise = spring({frame: f, fps, config: {damping: 16, stiffness: 80, mass: 1.1}});
  const titleIn = spring({frame: f - 10, fps, config: {damping: 14}});
  const titleOut = interpolate(f, [HOME_AT - 6, HOME_AT + 6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // HP turun & membesar sedikit setelah judul hilang
  const settle = interpolate(f, [HOME_AT - 6, HOME_AT + 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.2, 0.8, 0.2, 1)});
  const scale = 1 + settle * 0.1;
  const phoneTop = interpolate(settle, [0, 1], [560, 330]);
  const tilt = (1 - rise) * 35 + Math.sin(f / 40) * 2;
  const splash = interpolate(f, [HOME_AT - 4, HOME_AT + 6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fingerS = spring({frame: f - (TAP_AT - 22), fps, config: {damping: 16}});
  const press = interpolate(f, [TAP_AT, TAP_AT + 4, TAP_AT + 10], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fingerOut = interpolate(f, [TAP_AT + 10, TAP_AT + 20], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const ripple = interpolate(f, [TAP_AT, TAP_AT + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill>
      <Background />
      <FadeOut dur={dur}>
        {/* Judul perkenalan */}
        <div style={{position: 'absolute', top: 150, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, color: '#fff', opacity: titleIn * titleOut, transform: `translateY(${(1 - titleIn) * 40}px)`}}>
          <div style={{fontSize: 46, fontWeight: 700, color: C.soft}}>Kenalin,</div>
          <div style={{fontSize: 140, fontWeight: 800, letterSpacing: -4, lineHeight: 1}}>KasRapi</div>
          <div style={{fontSize: 44, fontWeight: 700, color: C.mint, marginTop: 14}}>Buku kas yang ngitung laba bersih</div>
        </div>

        {/* HP */}
        <div style={{position: 'absolute', left: '50%', top: phoneTop, transform: `translateX(-50%) translateY(${(1 - rise) * 1400}px) perspective(2000px) rotateX(${tilt}deg) rotateZ(${(1 - rise) * -10}deg) scale(${scale})`, transformOrigin: 'top center'}}>
          <Phone>
            {f >= HOME_AT - 4 && <AppHome start={HOME_AT} />}
            {f >= SHEET_AT && <AppSaleSheet start={SHEET_AT} />}
            {f < SHEET_AT && f >= HOME_AT - 4 && <BottomNav pressed={press} />}
            {/* splash */}
            <div style={{position: 'absolute', inset: 0, opacity: splash, background: `linear-gradient(160deg,${C.brand},#134e4a)`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 22, fontFamily: FONT, color: '#fff'}}>
              <div style={{width: 160, height: 160, borderRadius: 48, background: 'rgba(255,255,255,.15)', display: 'grid', placeItems: 'center'}}><IcChart size={96} /></div>
              <div style={{fontSize: 56, fontWeight: 800}}>KasRapi</div>
            </div>
            {/* riak ketukan */}
            {f >= TAP_AT && f < TAP_AT + 20 && (
              <div style={{position: 'absolute', left: '50%', bottom: 76, width: 220, height: 220, marginLeft: -110, marginBottom: -110, borderRadius: '50%', border: `6px solid ${C.brand2}`, transform: `scale(${ripple})`, opacity: 1 - ripple, zIndex: 40}} />
            )}
          </Phone>
          {/* jari */}
          <div style={{position: 'absolute', left: '50%', top: PHONE_H - 120, fontSize: 120, transform: `translate(-10%, ${(1 - fingerS) * 400 + press * 18}px)`, opacity: fingerS * fingerOut, zIndex: 60}}>👆</div>
        </div>

        <Callout text="Laba bersih langsung kelihatan" at={HOME_AT + 20} top={110} side="left" />
        <Callout text="Kanal mana paling untung?" at={HOME_AT + 100} top={110} side="right" color="#fde68a" />
        <Callout text="Potongan Shopee dihitung otomatis" at={SHEET_AT + 40} top={110} side="left" />
      </FadeOut>
    </AbsoluteFill>
  );
};
