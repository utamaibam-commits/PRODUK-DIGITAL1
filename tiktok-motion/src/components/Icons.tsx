import React from 'react';

type P = {size?: number; color?: string; stroke?: number};
const base = (size: number, color: string, stroke: number) => ({
  width: size,
  height: size,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: color,
  strokeWidth: stroke,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
});

export const IcChart: React.FC<P> = ({size = 40, color = '#fff', stroke = 2.2}) => (
  <svg {...base(size, color, stroke)}><path d="M3 3v18h18" /><path d="M7 15l4-4 3 3 6-7" /></svg>
);
export const IcAndroid: React.FC<P> = ({size = 40, color = '#fff', stroke = 1.9}) => (
  <svg {...base(size, color, stroke)}><path d="M5 10h14v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7Z" /><path d="M5 10a7 7 0 0 1 14 0" /><path d="m7 4 1.5 2.5M17 4l-1.5 2.5" /></svg>
);
export const IcApple: React.FC<P> = ({size = 40, color = '#fff', stroke = 1.9}) => (
  <svg {...base(size, color, stroke)}><path d="M16.5 12.6c0-2.3 1.9-3.4 2-3.5a4.3 4.3 0 0 0-3.4-1.8c-1.4-.2-2.8.8-3.5.8s-1.9-.8-3.1-.8A4.6 4.6 0 0 0 4.6 9.7c-1.7 2.9-.4 7.2 1.2 9.6.8 1.2 1.8 2.5 3 2.4s1.7-.8 3.1-.8 1.9.8 3.1.8 2.1-1.2 2.8-2.4a10 10 0 0 0 1.3-2.6 4 4 0 0 1-2.6-4.1Z" /><path d="M14.3 5.6A3.6 3.6 0 0 0 15.2 3a3.7 3.7 0 0 0-2.4 1.2 3.4 3.4 0 0 0-.9 2.5 3 3 0 0 0 2.4-1.1Z" /></svg>
);
export const IcLaptop: React.FC<P> = ({size = 40, color = '#fff', stroke = 1.9}) => (
  <svg {...base(size, color, stroke)}><rect x="4" y="5" width="16" height="11" rx="2" /><path d="M2 19h20" /></svg>
);
export const IcWifiOff: React.FC<P> = ({size = 40, color = '#fff', stroke = 2}) => (
  <svg {...base(size, color, stroke)}><path d="M2 8.8a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0" /><circle cx="12" cy="19.5" r="1" fill={color} /><path d="M3 3l18 18" /></svg>
);
export const IcCheck: React.FC<P> = ({size = 40, color = '#fff', stroke = 3}) => (
  <svg {...base(size, color, stroke)}><path d="m5 12 5 5L20 7" /></svg>
);
export const IcPlus: React.FC<P> = ({size = 40, color = '#fff', stroke = 2.6}) => (
  <svg {...base(size, color, stroke)}><path d="M12 5v14M5 12h14" /></svg>
);
export const IcArrowUp: React.FC<P> = ({size = 40, color = '#fff', stroke = 2.6}) => (
  <svg {...base(size, color, stroke)}><path d="M12 20V5M5 12l7-7 7 7" /></svg>
);
export const IcHome: React.FC<P> = ({size = 40, color = '#fff', stroke = 2}) => (
  <svg {...base(size, color, stroke)}><path d="M3 10.5 12 3l9 7.5" /><path d="M5 9.5V20h5v-6h4v6h5V9.5" /></svg>
);
export const IcList: React.FC<P> = ({size = 40, color = '#fff', stroke = 2}) => (
  <svg {...base(size, color, stroke)}><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01" /></svg>
);
export const IcBox: React.FC<P> = ({size = 40, color = '#fff', stroke = 2}) => (
  <svg {...base(size, color, stroke)}><path d="M21 8 12 3 3 8v8l9 5 9-5V8Z" /><path d="m3 8 9 5 9-5M12 13v8" /></svg>
);
export const IcShield: React.FC<P> = ({size = 40, color = '#fff', stroke = 2}) => (
  <svg {...base(size, color, stroke)}><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z" /><path d="m9 12 2 2 4-4" /></svg>
);
