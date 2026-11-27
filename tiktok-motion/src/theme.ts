import {loadFont} from '@remotion/google-fonts/PlusJakartaSans';

const {fontFamily} = loadFont('normal', {
  weights: ['500', '700', '800'],
  subsets: ['latin'],
});

export const FONT = fontFamily;

export const C = {
  bg: '#04211e',
  bg2: '#0b3b36',
  brand: '#0f766e',
  brand2: '#14b8a6',
  mint: '#5eead4',
  soft: '#ccfbf1',
  white: '#ffffff',
  ink: '#0f1f1c',
  ink2: '#47605b',
  ink3: '#7c918d',
  line: '#e2ebe9',
  surface2: '#f7faf9',
  appBg: '#f1f5f4',
  neg: '#f43f5e',
  pos: '#059669',
  warn: '#f59e0b',
  indigo: '#6366f1',
  orange: '#f97316',
  green: '#22c55e',
};

export const FPS = 30;

export const rp = (n: number) =>
  'Rp' + Math.round(n).toLocaleString('id-ID').replace(/,/g, '.');
