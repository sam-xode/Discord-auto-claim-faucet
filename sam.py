import samxode_ip
import time
import json
import sys
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Memuat .env atau membuatnya jika tidak ada
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("DISCORD_TOKENS={}\n")
        f.write("FAUCETS=[]\n")

load_dotenv()

def load_tokens():
    try:
        return json.loads(os.getenv("DISCORD_TOKENS", "{}"))
    except json.JSONDecodeError:
        return {}

def load_faucets():
    try:
        return json.loads(os.getenv("FAUCETS", "[]"))
    except json.JSONDecodeError:
        return []

def save_data():
    with open(".env", "w") as f:
        f.write(f"DISCORD_TOKENS={json.dumps(tokens)}\n")
        f.write(f"FAUCETS={json.dumps(faucets)}\n")

tokens = load_tokens()
faucets = load_faucets()
claim_times = {}
skip_channels = {}

def parse_time_input(time_input):
    if "h" in time_input:
        return int(time_input.replace("h", "")) * 3600
    elif "m" in time_input:
        return int(time_input.replace("m", "")) * 60
    else:
        raise ValueError("Format waktu tidak valid. Gunakan 'h' atau 'm'.")

def format_time(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    minutes %= 60
    return f"{hours} jam {minutes} menit" if hours > 0 else f"{minutes} menit"

def claim_faucet(faucet_name, channel_id, messages, delay):
    global claim_times, skip_channels
    now = datetime.now()
    
    if channel_id not in tokens:
        print(f"\n❌ [ERROR] Tidak ada token yang terdaftar untuk channel {channel_id}")
        return
    
    for i, token in enumerate(tokens[channel_id]):
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"content": messages[i % len(messages)]}  # Pesan berbeda tiap token
        
        try:
            response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"\n❌ [ERROR] Admin tidak memberikan mu izin untuk mengirim [{faucet_name}] ke channel: {channel_id}")
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after", 0)
                skip_channels[channel_id] = datetime.now() + timedelta(seconds=retry_after)
                print(f"\n⚠️  [SLOWMODE] {faucet_name} terkena slowmode, menunggu {format_time(retry_after)}")
            else:
                print(f"\n❌ [GAGAL] {faucet_name} tidak diklaim. Status: {response.status_code}")
            continue
        
        if response.status_code == 200:
            claim_times[faucet_name] = datetime.now()
            print(f"\n✅ [SUKSES] {faucet_name} berhasil diklaim di Channel: {channel_id} oleh Token ke-{i+1}")

def main():
    while True:
        print("\nPilih opsi:")
        print("1. CLAIM SEMUA FAUCET")
        print("2. Tambah pesan baru untuk CLAIM FAUCET")
        print("3. Tampilkan daftar channel yang terkena slowmode")
        print("4. Keluar")
        choice = input("Masukkan pilihan (1/2/3/4): ")
        
        if choice == "1":
            if not faucets:
                print("\n⚠️  Tidak ada faucet yang disimpan. Tambahkan faucet dulu di opsi 2.")
                continue
            print("\n✅ Memulai claim faucet...")
            for faucet in faucets:
                claim_faucet(*faucet)
        
        elif choice == "2":
            channel_id = input("Masukkan Channel ID: ")
            tokens_input = input("Masukkan daftar DISCORD_TOKENS (dipisahkan dengan koma): ").split(",")
            tokens[channel_id] = [t.strip() for t in tokens_input if t.strip()]
            
            faucet_name = input("Masukkan nama faucet: ")
            messages = input("Masukkan pesan-pesan yang ingin dikirim (pisahkan dengan |): ").split("|")
            delay_input = input("Masukkan waktu claim ulang otomatis (misal: 6h atau 30m): ")
            
            try:
                delay = parse_time_input(delay_input)
                faucets.append((faucet_name, channel_id, messages, delay))
                save_data()
                print(f"\n✅ [FAUCET DITAMBAHKAN] {faucet_name} disimpan!")
            except ValueError as e:
                print(f"❌ [ERROR] {e}")
        
        elif choice == "3":
            if skip_channels:
                print("\n⚠️  Daftar channel yang terkena slowmode:")
                for channel_id, wait_time in skip_channels.items():
                    remaining_time = (wait_time - datetime.now()).total_seconds()
                    faucet_name = next((f[0] for f in faucets if f[1] == channel_id), channel_id)
                    print(f"- {faucet_name}, Slowmode: {format_time(remaining_time)}")
            else:
                print("\n✅ Tidak ada channel yang terkena slowmode.")
        
        elif choice == "4":
            print("\nProgram berhenti. Terima kasih telah menggunakan <SAMXODE/>\n")
            sys.exit(0)
        
        else:
            print("❌ Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna. Terima kasih sudah menggunakan <SAMXODE/>")
        sys.exit(0)
