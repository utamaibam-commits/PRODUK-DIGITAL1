import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {C, FONT, rp} from '../theme';
import {IcBox, IcChart, IcHome, IcList, IcPlus} from './Icons';

// Tiruan setia tampilan Beranda Aplikasi-UMKM.html (KasRapi) di dalam layar HP.
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);

const Card: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div
    style={{
      background: '#fff',
      borderRadius: 26,
      border: `1px solid ${C.line}`,
      boxShadow: '0 10px 26px -14px rgba(15,31,28,.25)',
      padding: 20,
      ...style,
    }}
  >
    {children}
  </div>
);

const Dot: React.FC<{c: string}> = ({c}) => (
  <span style={{width: 11, height: 11, borderRadius: 9, background: c, display: 'inline-block'}} />
);

const count = (t: number, to: number) => to * ease(Math.min(Math.max(t, 0), 1));

export const AppHome: React.FC<{start?: number}> = ({start = 0}) => {
  const frame = useCurrentFrame() - start;
  const t = (a: number, d: number) => (frame - a) / d;
  const bars = [
    [0.55, 0.1], [0.12, 0], [0.62, 0.2], [0.5, 0.22], [0.27, 0], [0.58, 0.05], [0.95, 0.12],
  ];
  const days = ['Sab', 'Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Ini'];
  const donut = [
    {n: 'WhatsApp', v: 28, c: C.green},
    {n: 'TikTok Shop', v: 25, c: C.indigo},
    {n: 'Shopee', v: 24, c: C.orange},
    {n: 'Offline', v: 13, c: C.brand},
    {n: 'GoFood', v: 10, c: C.neg},
  ];
  const R = 58;
  const CIRC = 2 * Math.PI * R;
  const dT = ease(Math.min(Math.max(t(30, 40), 0), 1));
  let off = 0;
  const appear = (i: number) => {
    const s = interpolate(frame, [i * 5, i * 5 + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
    return {opacity: s, transform: `translateY(${(1 - s) * 30}px)`};
  };
  return (
    <div style={{fontFamily: FONT, color: C.ink, position: 'absolute', inset: 0, background: C.appBg}}>
      {/* top bar */}
      <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '84px 26px 14px'}}>
        <div style={{width: 54, height: 54, borderRadius: 17, background: `linear-gradient(135deg,${C.brand},${C.brand2})`, display: 'grid', placeItems: 'center'}}>
          <IcChart size={30} />
        </div>
        <div>
          <div style={{fontWeight: 800, fontSize: 26, lineHeight: 1.1}}>Beranda</div>
          <div style={{fontSize: 17, color: C.ink3, fontWeight: 600}}>Dapur Bu Rina</div>
        </div>
      </div>
      <div style={{padding: '0 22px', display: 'flex', flexDirection: 'column', gap: 16}}>
        {/* hero */}
        <div style={{...appear(0), borderRadius: 32, padding: 24, color: '#fff', background: `radial-gradient(120% 140% at 100% 0%, #2dd4bf 0%, transparent 55%), linear-gradient(135deg,#0f766e,#115e59 55%,#134e4a)`, boxShadow: '0 24px 40px -22px #0f766e'}}>
          <div style={{fontSize: 18, opacity: 0.85, fontWeight: 700}}>Saldo kas usaha</div>
          <div style={{fontSize: 46, fontWeight: 800, letterSpacing: -1, margin: '4px 0 16px', fontVariantNumeric: 'tabular-nums'}}>{rp(count(t(4, 40), 15597670))}</div>
          <div style={{display: 'flex', gap: 12}}>
            {[['Laba bersih November', rp(count(t(10, 40), 3079670))], ['Margin bersih', Math.round(count(t(10, 40), 24)) + '%']].map(([k, v]) => (
              <div key={k} style={{flex: 1, background: 'rgba(255,255,255,.13)', border: '1px solid rgba(255,255,255,.18)', borderRadius: 20, padding: '12px 14px'}}>
                <div style={{fontSize: 14, opacity: 0.85, fontWeight: 700}}>{k}</div>
                <div style={{fontSize: 22, fontWeight: 800, fontVariantNumeric: 'tabular-nums'}}>{v}</div>
              </div>
            ))}
          </div>
        </div>
        {/* stats */}
        <div style={{...appear(2), display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14}}>
          {[['Omzet bulan ini', 13077000, C.brand], ['Potongan kanal', 1157330, C.warn]].map(([k, v, c]) => (
            <Card key={k as string} style={{padding: 18}}>
              <div style={{fontSize: 15, color: C.ink3, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8}}><Dot c={c as string} />{k}</div>
              <div style={{fontSize: 26, fontWeight: 800, marginTop: 4, fontVariantNumeric: 'tabular-nums'}}>{rp(count(t(8, 36), v as number))}</div>
            </Card>
          ))}
        </div>
        {/* bar chart */}
        <Card style={appear(4)}>
          <div style={{fontWeight: 800, fontSize: 20, marginBottom: 12}}>Arus kas 7 hari</div>
          <div style={{display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: 150, borderBottom: `1px dashed ${C.line}`}}>
            {bars.map(([a, b], i) => {
              const g = ease(Math.min(Math.max(t(18 + i * 3, 26), 0), 1));
              return (
                <div key={i} style={{display: 'flex', gap: 5, alignItems: 'flex-end', height: '100%'}}>
                  <div style={{width: 22, height: `${a * 100 * g}%`, background: C.brand, borderRadius: 7}} />
                  <div style={{width: 22, height: `${b * 100 * g}%`, background: C.neg, opacity: 0.85, borderRadius: 7}} />
                </div>
              );
            })}
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 14, color: C.ink3, fontWeight: 700}}>
            {days.map((d) => <span key={d} style={{width: 49, textAlign: 'center'}}>{d}</span>)}
          </div>
        </Card>
        {/* donut */}
        <Card style={{...appear(6), display: 'flex', alignItems: 'center', gap: 20}}>
          <svg width="150" height="150" viewBox="0 0 150 150">
            {donut.map((d) => {
              const len = (CIRC * d.v) / 100;
              const el = (
                <circle key={d.n} cx="75" cy="75" r={R} fill="none" stroke={d.c} strokeWidth="20"
                  strokeDasharray={`${Math.max(len * dT - 3, 0.01)} ${CIRC}`} strokeDashoffset={-off * dT} transform="rotate(-90 75 75)" />
              );
              off += len;
              return el;
            })}
            <text x="75" y="70" textAnchor="middle" fontSize="13" fill={C.ink3} fontWeight="700" fontFamily={FONT}>Omzet</text>
            <text x="75" y="92" textAnchor="middle" fontSize="20" fill={C.ink} fontWeight="800" fontFamily={FONT}>13,1 jt</text>
          </svg>
          <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 7, fontSize: 17, fontWeight: 600}}>
            {donut.map((d) => (
              <div key={d.n} style={{display: 'flex', alignItems: 'center', gap: 9}}><Dot c={d.c} /><span>{d.n}</span><b style={{marginLeft: 'auto'}}>{d.v}%</b></div>
            ))}
          </div>
        </Card>
      </div>
      <BottomNav />
    </div>
  );
};

export const BottomNav: React.FC<{pressed?: number}> = ({pressed = 0}) => (
  <div style={{position: 'absolute', left: 16, right: 16, bottom: 22, height: 92, borderRadius: 32, background: 'rgba(255,255,255,.94)', border: `1px solid ${C.line}`, boxShadow: '0 20px 50px -20px rgba(15,31,28,.45)', display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', alignItems: 'center', fontFamily: FONT, zIndex: 20}}>
    {[[IcHome, 'Beranda'], [IcList, 'Transaksi']].map(([I, l], i) => {
      const Ic = I as typeof IcHome;
      return (
        <div key={l as string} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, color: i === 0 ? C.brand : C.ink3, fontSize: 13, fontWeight: 700}}>
          <Ic size={28} color={i === 0 ? C.brand : C.ink3} />{l as string}
        </div>
      );
    })}
    <div style={{justifySelf: 'center', width: 76, height: 76, marginTop: -36, borderRadius: 25, background: `linear-gradient(135deg,${C.brand},${C.brand2})`, display: 'grid', placeItems: 'center', boxShadow: `0 14px 26px -8px ${C.brand}`, transform: `scale(${1 - pressed * 0.12}) rotate(${pressed * 90}deg)`}}>
      <IcPlus size={38} />
    </div>
    {[[IcBox, 'Stok'], [IcChart, 'Laporan']].map(([I, l]) => {
      const Ic = I as typeof IcHome;
      return (
        <div key={l as string} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, color: C.ink3, fontSize: 13, fontWeight: 700}}>
          <Ic size={28} color={C.ink3} />{l as string}
        </div>
      );
    })}
  </div>
);

// Lembar "Catat Penjualan" yang naik dari bawah, menghitung laba bersih langkah demi langkah.
export const AppSaleSheet: React.FC<{start: number}> = ({start}) => {
  const frame = useCurrentFrame() - start;
  const {fps} = useVideoConfig();
  const up = spring({frame, fps, config: {damping: 18, stiffness: 120}});
  const line = (i: number) => interpolate(frame, [22 + i * 14, 34 + i * 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const qtyT = interpolate(frame, [14, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const qty = qtyT >= 1 ? 3 : 1;
  const rows: [string, string, string][] = [
    ['Omzet', rp(45000), C.ink],
    ['Potongan Shopee (12% + Rp1.250)', '-' + rp(6650), C.neg],
    ['Modal (HPP) 3×Rp8.000', '-' + rp(24000), C.neg],
  ];
  const tot = line(3);
  const pulse = 1 + Math.sin(Math.max(frame - 64, 0) / 4) * 0.04 * (frame > 64 && frame < 100 ? 1 : 0);
  const field = (label: string, value: string, active = false) => (
    <div style={{marginBottom: 14}}>
      <div style={{fontSize: 15, fontWeight: 800, color: C.ink2, marginBottom: 6}}>{label}</div>
      <div style={{padding: '15px 18px', borderRadius: 18, border: `2px solid ${active ? C.brand : C.line}`, background: C.surface2, fontSize: 21, fontWeight: 600, boxShadow: active ? `0 0 0 5px ${C.brand}22` : 'none'}}>{value}</div>
    </div>
  );
  return (
    <>
      <div style={{position: 'absolute', inset: 0, background: 'rgba(5,15,13,.45)', opacity: up, zIndex: 30}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: '82%', background: '#fff', borderRadius: '36px 36px 0 0', padding: '16px 24px', transform: `translateY(${(1 - up) * 100}%)`, zIndex: 31, fontFamily: FONT, color: C.ink}}>
        <div style={{width: 60, height: 7, borderRadius: 9, background: C.line, margin: '0 auto 18px'}} />
        <div style={{fontSize: 28, fontWeight: 800, marginBottom: 16}}>Catat Penjualan</div>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 4, padding: 5, borderRadius: 20, background: C.surface2, border: `1px solid ${C.line}`, marginBottom: 16}}>
          {['Jual', 'Biaya', 'Stok', 'Pribadi', 'Modal'].map((s, i) => (
            <div key={s} style={{textAlign: 'center', padding: '10px 0', borderRadius: 15, fontSize: 16, fontWeight: 800, background: i === 0 ? '#fff' : 'transparent', color: i === 0 ? C.brand : C.ink2, boxShadow: i === 0 ? '0 4px 12px -6px rgba(0,0,0,.25)' : 'none'}}>{s}</div>
          ))}
        </div>
        {field('Produk', 'Keripik Pisang Coklat (stok 60)')}
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12}}>
          {field('Jumlah', String(qty), frame > 8 && frame < 24)}
          {field('Harga satuan', '15.000')}
        </div>
        {field('Kanal penjualan', 'Shopee')}
        <div style={{borderRadius: 20, border: `2px dashed ${C.line}`, background: C.surface2, padding: '14px 18px', fontSize: 18}}>
          {rows.map(([k, v, c], i) => (
            <div key={k} style={{display: 'flex', justifyContent: 'space-between', padding: '5px 0', color: C.ink2, opacity: line(i), transform: `translateX(${(1 - line(i)) * 30}px)`}}>
              <span>{k}</span><b style={{color: c, fontVariantNumeric: 'tabular-nums'}}>{v}</b>
            </div>
          ))}
          <div style={{display: 'flex', justifyContent: 'space-between', borderTop: `1px solid ${C.line}`, marginTop: 8, paddingTop: 10, fontSize: 24, fontWeight: 800, opacity: tot, transform: `scale(${pulse})`, transformOrigin: 'right center'}}>
            <span>Laba bersih</span><span style={{color: C.pos, fontVariantNumeric: 'tabular-nums'}}>{rp(count(tot, 14350))}</span>
          </div>
        </div>
      </div>
    </>
  );
};
