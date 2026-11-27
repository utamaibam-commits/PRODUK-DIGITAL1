import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Background} from '../components/Background';
import {IcAndroid, IcApple, IcCheck, IcLaptop, IcShield, IcWifiOff} from '../components/Icons';
import {FadeOut, PopWords} from '../components/Text';
import {C, FONT} from '../theme';

const DEVICES = [
  {Ic: IcAndroid, label: 'Android'},
  {Ic: IcApple, label: 'iPhone'},
  {Ic: IcLaptop, label: 'Laptop'},
];

export const Offline: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const wifi = spring({frame: f - 50, fps, config: {damping: 10}});
  return (
    <AbsoluteFill>
      <Background />
      <FadeOut dur={dur}>
        <AbsoluteFill style={{fontFamily: FONT, color: '#fff', alignItems: 'center', padding: '200px 80px 0'}}>
          <PopWords text="Jalan di HP *apa* aja" size={96} />
          <div style={{display: 'flex', gap: 30, marginTop: 60}}>
            {DEVICES.map(({Ic, label}, i) => {
              const s = spring({frame: f - 10 - i * 7, fps, config: {damping: 12, stiffness: 150}});
              const chk = spring({frame: f - 26 - i * 7, fps, config: {damping: 9}});
              return (
                <div key={label} style={{width: 270, height: 300, borderRadius: 44, background: 'rgba(255,255,255,.08)', border: '2px solid rgba(255,255,255,.18)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 18, transform: `perspective(900px) rotateY(${(1 - s) * 90}deg)`, opacity: s, position: 'relative'}}>
                  <Ic size={110} color={C.mint} />
                  <div style={{fontSize: 44, fontWeight: 800}}>{label}</div>
                  <div style={{position: 'absolute', top: -22, right: -22, width: 76, height: 76, borderRadius: 40, background: C.green, display: 'grid', placeItems: 'center', transform: `scale(${chk})`, boxShadow: '0 10px 20px -6px rgba(0,0,0,.5)'}}><IcCheck size={46} /></div>
                </div>
              );
            })}
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: 36, marginTop: 90, transform: `scale(${wifi})`}}>
            <div style={{position: 'relative', width: 170, height: 170, borderRadius: 50, background: C.neg, display: 'grid', placeItems: 'center'}}>
              <IcWifiOff size={110} />
            </div>
            <div>
              <div style={{fontSize: 86, fontWeight: 800, lineHeight: 1}}>100% OFFLINE</div>
              <div style={{fontSize: 46, fontWeight: 700, color: C.soft, position: 'relative', display: 'inline-block', marginTop: 8}}>
                Tanpa kuota internet
              </div>
            </div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 20, marginTop: 80, width: '100%'}}>
            {['Sekali bayar, tanpa langganan bulanan', 'Data cuma tersimpan di HP kamu', 'Panduan Android & iPhone disertakan'].map((t, i) => {
              const s = spring({frame: f - 76 - i * 8, fps, config: {damping: 14}});
              return (
                <div key={t} style={{display: 'flex', alignItems: 'center', gap: 22, fontSize: 46, fontWeight: 700, transform: `translateX(${(1 - s) * -200}px)`, opacity: s}}>
                  <div style={{width: 64, height: 64, borderRadius: 20, background: C.brand2, display: 'grid', placeItems: 'center', flex: 'none'}}>{i === 1 ? <IcShield size={38} /> : <IcCheck size={38} />}</div>
                  {t}
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      </FadeOut>
    </AbsoluteFill>
  );
};
