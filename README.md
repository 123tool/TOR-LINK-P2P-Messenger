### Langkah 1: Instalasi Lingkungan (Termux/Linux/CMD)
​Jalankan perintah ini di terminal Anda:
​Untuk Termux:
```bash
pkg update && pkg upgrade
pkg install tor python -y
pip install stem flask requests pysocks

```
Untuk Linux (Ubuntu/Kali):
```bash
sudo apt update && sudo apt install tor -y
pip install stem flask requests pysocks
```

### Langkah 2: Konfigurasi Tor (PENTING)
​Agar script bisa mengontrol Tor, Anda harus mengaktifkan ControlPort.
Cari file torrc.
​Termux: 
```bash
/data/data/com.termux/files/usr/etc/tor/torrc
​Linux: /etc/tor/torrc
```
Tambahkan atau hapus tanda # pada baris berikut:
```bash
ControlPort 9051
CookieAuthentication 0
```
Restart Tor:
```bash
​Termux : pkill tor lalu ketik tor di session baru.
​Linux : sudo service tor restart
```

### Panduan Penggunaan
***​Jalankan Aplikasi:***
Buka terminal dan ketik python tor_link.py

​Dapatkan Alamat :
Aplikasi akan menampilkan alamat unik Anda
```bash
(contoh: v2c3...xyz.onion).***
```
***​Kirim Pesan:
Minta teman Anda menjalankan script yang sama, lalu masukkan alamat .onion mereka di menu "Kirim Pesan".***

***​Tanpa Port Forwarding:
Karena lewat jalur Tor, Anda tidak perlu setting router. Aplikasi ini bisa menembus jaringan kantor, sekolah, atau provider seluler sekalipun.***

### ​📝 Catatan :
***​Enkripsi: Anda bisa menambahkan library cryptography (RSA) agar pesan dienkripsi sebelum masuk ke jaringan Tor.***
