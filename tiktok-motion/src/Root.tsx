import React from 'react';
import {Composition} from 'remotion';
import {KasRapiPromo} from './KasRapiPromo';

// 3 variasi hook. Ubah teks langsung di Remotion Studio (panel Props) atau di sini.
// Kata yang diapit *bintang* mendapat sorotan stabilo.
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="KasRapi-V1-UangKemana"
      component={KasRapiPromo}
      durationInFrames={840}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        kicker: 'OMZET 13 JUTA…',
        line1: 'Kok saldo tinggal *segini?*',
        line2: 'Uangnya ke mana?',
        emoji: '😩',
        price: 'Rp59rb',
        lynkUrl: 'lynk.id/ibam2178',
        voiceover: 'audio/vo-v1.wav',
        voiceoverStart: 0,
      }}
    />
    <Composition
      id="KasRapi-V2-PotonganShopee"
      component={KasRapiPromo}
      durationInFrames={840}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        kicker: 'SELLER SHOPEE WAJIB TAHU',
        line1: 'Jual *Rp45.000*',
        line2: 'untungmu cuma Rp14.350',
        emoji: '😱',
        price: 'Rp59rb',
        lynkUrl: 'lynk.id/ibam2178',
        voiceover: 'audio/vo-v2.wav',
        voiceoverStart: 0,
      }}
    />
    <Composition
      id="KasRapi-V3-UangDapur"
      component={KasRapiPromo}
      durationInFrames={840}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        kicker: 'CUMA 46% UMKM YANG MISAHIN',
        line1: 'Uang dagangan buat *belanja* *dapur?*',
        line2: 'Kamu nggak sendiri',
        emoji: '🍳',
        price: 'Rp59rb',
        lynkUrl: 'lynk.id/ibam2178',
        voiceover: 'audio/vo-v3.wav',
        voiceoverStart: 0,
      }}
    />
  </>
);
