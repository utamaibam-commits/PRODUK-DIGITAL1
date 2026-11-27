import React from 'react';
import {AbsoluteFill, Series} from 'remotion';
import {AppDemo} from './scenes/AppDemo';
import {CTA} from './scenes/CTA';
import {Hook} from './scenes/Hook';
import {Offline} from './scenes/Offline';
import {Problem} from './scenes/Problem';

export type PromoProps = {
  readonly kicker: string;
  readonly line1: string;
  readonly line2: string;
  readonly emoji: string;
  readonly price: string;
  readonly lynkUrl: string;
};

// Durasi tiap adegan (30 fps). Total 840 frame = 28 detik.
export const D = {hook: 90, problem: 150, demo: 330, offline: 150, cta: 120};
export const TOTAL = D.hook + D.problem + D.demo + D.offline + D.cta;

export const KasRapiPromo: React.FC<PromoProps> = ({kicker, line1, line2, emoji, price, lynkUrl}) => (
  <AbsoluteFill style={{backgroundColor: '#04211e'}}>
    <Series>
      <Series.Sequence name="1 Hook" durationInFrames={D.hook}>
        <Hook kicker={kicker} line1={line1} line2={line2} emoji={emoji} dur={D.hook} />
      </Series.Sequence>
      <Series.Sequence name="2 Masalah" durationInFrames={D.problem}>
        <Problem dur={D.problem} />
      </Series.Sequence>
      <Series.Sequence name="3 Solusi + Demo App" durationInFrames={D.demo}>
        <AppDemo dur={D.demo} />
      </Series.Sequence>
      <Series.Sequence name="4 Offline Android & iPhone" durationInFrames={D.offline}>
        <Offline dur={D.offline} />
      </Series.Sequence>
      <Series.Sequence name="5 CTA" durationInFrames={D.cta}>
        <CTA price={price} lynkUrl={lynkUrl} />
      </Series.Sequence>
    </Series>
  </AbsoluteFill>
);
