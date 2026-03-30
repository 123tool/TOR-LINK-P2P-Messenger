import os
import sys
import threading
import time
import sqlite3
from flask import Flask, request
from stem.control import Controller
import requests

# --- KONFIGURASI ---
LOCAL_PORT = 5000  # Port aplikasi lokal
TOR_CONTROL_PORT = 9051  # Port kontrol Tor
TOR_SOCKS_PORT = 9050    # Port proxy SOCKS Tor
SESSIONS = requests.Session()
SESSIONS.proxies = {'http': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
                    'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'}

app = Flask(__name__)

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts 
                 (alias TEXT, onion_address TEXT)''')
    conn.commit()
    conn.close()

# --- SERVER RECEIVER (Menerima Pesan) ---
@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    sender = data.get('sender', 'Unknown')
    msg = data.get('message', '')
    print(f"\n\n[PESAN BARU DARI {sender}]: {msg}")
    print("Kirim pesan (Ketik 'menu' untuk opsi): ", end="")
    return {"status": "success"}, 200

def run_flask():
    app.run(port=LOCAL_PORT, debug=False, use_reloader=False)

# --- TOR HIDDEN SERVICE LOGIC ---
def start_tor_service():
    print("[*] Menghubungkan ke Tor Control Port...")
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate() # Sesuaikan jika Tor Anda pakai password
            
            # Membuat atau memuat Hidden Service
            key_path = os.path.join(os.getcwd(), "keys")
            if not os.path.exists(key_path): os.makedirs(key_path)
            
            # Setup Hidden Service (Port 80 Tor -> Port 5000 Lokal)
            print("[*] Mengaktifkan Hidden Service (Tunggu sebentar)...")
            result = controller.create_ephemeral_hidden_service({80: LOCAL_PORT}, await_publication=True)
            onion_url = f"{result.service_id}.onion"
            
            print(f"\n{'='*40}")
            print(f" ALAMAT ONION ANDA: {onion_url}")
            print(f"{'='*40}\n")
            return onion_url
    except Exception as e:
        print(f"[!] Gagal konek ke Tor: {e}")
        print("[!] Pastikan 'tor' sudah jalan dan 'ControlPort 9051' aktif di torrc.")
        sys.exit()

# --- CLIENT LOGIC (Mengirim Pesan) ---
def send_message(target_onion, my_address):
    msg = input("Isi Pesan: ")
    url = f"http://{target_onion}/receive"
    payload = {"sender": my_address, "message": msg}
    try:
        print("[*] Mengirim melalui jaringan Tor...")
        SESSIONS.post(url, json=payload, timeout=30)
        print("[+] Pesan Terkirim!")
    except Exception as e:
        print(f"[-] Gagal mengirim: {e}")

# --- MAIN MENU ---
def main():
    init_db()
    # Jalankan Server di Background
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Jalankan Tor Service
    my_onion = start_tor_service()

    while True:
        print("\n--- MENU TOR-LINK ---")
        print("1. Kirim Pesan Langsung")
        print("2. Tambah Kontak")
        print("3. Lihat Kontak")
        print("4. Keluar")
        choice = input("Pilih: ")

        if choice == '1':
            target = input("Masukkan Alamat .onion tujuan: ")
            send_message(target, my_onion)
        elif choice == '2':
            alias = input("Nama Alias: ")
            addr = input("Alamat .onion: ")
            conn = sqlite3.connect('contacts.db')
            conn.execute("INSERT INTO contacts VALUES (?, ?)", (alias, addr))
            conn.commit()
            conn.close()
            print("[+] Kontak disimpan.")
        elif choice == '3':
            conn = sqlite3.connect('contacts.db')
            for row in conn.execute("SELECT * FROM contacts"):
                print(f"- {row[0]}: {row[1]}")
            conn.close()
        elif choice == '4':
            break

if __name__ == "__main__":
    main()
