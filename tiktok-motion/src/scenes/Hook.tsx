import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Background} from '../components/Background';
import {FadeOut, PopWords} from '../components/Text';
import {C, FONT} from '../theme';

export type HookProps = {
  readonly kicker: string;
  readonly line1: string;
  readonly line2: string;
  readonly emoji: string;
};

export const Hook: React.FC<HookProps & {dur: number}> = ({kicker, line1, line2, emoji, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k = spring({frame: f, fps, config: {damping: 14}});
  const e = spring({frame: f - 22, fps, config: {damping: 8, stiffness: 160}});
  const shake = Math.sin(f / 2.2) * 6 * interpolate(f, [24, 60], [1, 0.3], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const flash = interpolate(f, [0, 6], [0.9, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <Background tint={C.neg} />
      <FadeOut dur={dur} out={8}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: '0 90px', gap: 34}}>
          <div style={{fontFamily: FONT, fontSize: 40, fontWeight: 800, color: C.bg, background: C.mint, padding: '12px 28px', borderRadius: 99, transform: `scale(${k}) rotate(${(1 - k) * -8}deg)`, letterSpacing: 1}}>
            {kicker}
          </div>
          <PopWords text={line1} size={104} delay={4} highlight={C.neg} />
          <PopWords text={line2} size={104} delay={14} color={C.mint} highlight={C.brand} />
          <div style={{fontSize: 150, transform: `scale(${e}) rotate(${shake}deg)`, marginTop: 10}}>{emoji}</div>
        </AbsoluteFill>
      </FadeOut>
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
};
