import json
B=json.load(open('/tmp/claude-0/kr/vo/beats.json'))
BEATS={1:[0,2.21,3.38,4.31],2:[0,1.97,2.72,3.98],3:[0,1.0,1.8,2.4],4:[0,1.4,3.65],5:[0,1.39,2.3],6:[0,2.45],7:[0,1.6,3.56]}
CAP={1:["Jualan di Shopee, TikTok, WhatsApp.","Tapi untung bersihnya berapa?","Gak tau, anjir.","Tenang, ada KasRapi!"],
2:["Catat penjualan cuma 5 detik.","Pilih kanal,","potongan Shopee langsung kehitung.","Laba bersihnya langsung keluar!"],
3:["Buka beranda.","Saldo kas,","omzet,","sampai margin, langsung kelihatan."],
4:["Kanal mana yang paling cuan?","Ada grafik omzet dan laba per kanal.","Anjay!"],
5:["Stok produk kepantau.","Kasbon pelanggan?","Gak bakal lupa lagi."],
6:["Laporan laba rugi sebulan, beres.","Kirim ke WhatsApp, atau simpan PDF."],
7:["Data aman di HP kamu sendiri.","Sekali bayar, gak ada langganan.","Cek link di bio sekarang!"]}
LEAD=0.3
SC=[];t=0
for s in range(1,8):
    d=B[str(s)]['dur'];tail=1.6 if s==7 else 0.55
    if s==1: tail=0.75
    D=LEAD+d+tail
    SC.append(dict(i=s,start=t,dur=D,vdur=d,beats=[LEAD+b for b in BEATS[s]]));t+=D
TOTAL=t
def caps():
    out=[]
    for sc in SC:
        bs=sc['beats']+[LEAD+sc['vdur']+0.15]
        for k,txt in enumerate(CAP[sc['i']]):
            w=txt.split();n=len(w);chunks=[w[i:i+4] for i in range(0,n,4)]
            a,b=sc['start']+bs[k],sc['start']+bs[k+1];acc=0
            for c in chunks:
                ca=a+(b-a)*acc/n;acc+=len(c);cb=a+(b-a)*acc/n
                out.append((ca,cb,' '.join(c)))
    return out
