import React from 'react';
import {Audio, interpolate, Sequence, staticFile} from 'remotion';

// Semua frame di bawah adalah frame global (30 fps) dan mengikuti waktu animasi tiap adegan:
// Hook 0-90 · Masalah 90-240 · Demo 240-570 · Offline 570-720 · CTA 720-840.
type Hit = {at: number; sfx: string; vol?: number};

const HITS: Hit[] = [
  // 1 Hook
  {at: 0, sfx: 'impact', vol: 0.9},
  {at: 2, sfx: 'pop', vol: 0.6},
  {at: 6, sfx: 'swipe', vol: 0.35},
  {at: 16, sfx: 'swipe', vol: 0.35},
  {at: 24, sfx: 'pop', vol: 0.8},
  {at: 84, sfx: 'whoosh', vol: 0.7},
  // 2 Masalah: tiap potongan "mencakar" omzet
  {at: 114, sfx: 'minus', vol: 0.7},
  {at: 136, sfx: 'minus', vol: 0.7},
  {at: 158, sfx: 'minus', vol: 0.7},
  {at: 186, sfx: 'impact', vol: 0.6},
  {at: 202, sfx: 'pop', vol: 0.8},
  {at: 230, sfx: 'riser', vol: 0.5},
  // 3 Solusi + demo aplikasi
  {at: 240, sfx: 'whoosh', vol: 0.8},
  {at: 306, sfx: 'swipe', vol: 0.5},
  {at: 330, sfx: 'pop', vol: 0.8},
  {at: 410, sfx: 'pop', vol: 0.8},
  {at: 440, sfx: 'tap', vol: 1},
  {at: 450, sfx: 'whoosh', vol: 0.5},
  {at: 472, sfx: 'tap', vol: 0.5},
  {at: 486, sfx: 'minus', vol: 0.45},
  {at: 500, sfx: 'minus', vol: 0.45},
  {at: 514, sfx: 'ding', vol: 0.8},
  {at: 490, sfx: 'pop', vol: 0.7},
  {at: 564, sfx: 'whoosh', vol: 0.7},
  // 4 Offline & perangkat
  {at: 596, sfx: 'check', vol: 0.7},
  {at: 603, sfx: 'check', vol: 0.7},
  {at: 610, sfx: 'check', vol: 0.7},
  {at: 620, sfx: 'impact', vol: 0.5},
  {at: 646, sfx: 'pop', vol: 0.6},
  {at: 654, sfx: 'pop', vol: 0.6},
  {at: 662, sfx: 'pop', vol: 0.6},
  {at: 714, sfx: 'whoosh', vol: 0.7},
  // 5 CTA
  {at: 720, sfx: 'pop', vol: 0.7},
  {at: 732, sfx: 'impact', vol: 0.7},
  {at: 740, sfx: 'ding', vol: 0.9},
  {at: 746, sfx: 'pop', vol: 0.8},
];

export const SoundTrack: React.FC<{voiceover: string; voiceoverStart: number}> = ({voiceover, voiceoverStart}) => {
  const hasVo = voiceover !== '';
  return (
    <>
      {/* Musik latar sintetis buatan sendiri (bebas hak cipta). Lebih pelan saat ada voiceover. */}
      <Audio
        src={staticFile('audio/music.wav')}
        volume={(f) => interpolate(f, [0, 10, 800, 840], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) * (hasVo ? 0.14 : 0.32)}
      />
      {hasVo && (
        <Sequence from={voiceoverStart} name="Voiceover">
          <Audio src={staticFile(voiceover)} volume={1} />
        </Sequence>
      )}
      {HITS.map((h, i) => (
        <Sequence key={i} from={h.at} durationInFrames={45} name={`SFX ${h.sfx}`}>
          <Audio src={staticFile(`audio/sfx/${h.sfx}.wav`)} volume={(h.vol ?? 0.7) * (hasVo ? 0.6 : 0.75)} />
        </Sequence>
      ))}
    </>
  );
};
