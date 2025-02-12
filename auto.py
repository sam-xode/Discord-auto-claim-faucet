import os
import time
import requests
import logging
from dotenv import dotenv_values
import threading
import re
import sys

# Konfigurasi logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Bot started!")

# Load environment variables
def load_config():
    return dotenv_values(".env")

config = load_config()
TOKEN = config.get("DISCORD_TOKEN")
SLOW_MODE_TRACKER = {}

# Fungsi untuk memformat mention user
def format_message(message):
    match = re.match(r"@(\d+)\s(.+)", message)
    if match:
        user_id, content = match.groups()
        return f"<@{user_id}> {content}", user_id
    return message, None

# Fungsi untuk mengirim pesan ke satu channel
def send_message(channel_id, message):
    global SLOW_MODE_TRACKER
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {"Authorization": f"{TOKEN}", "Content-Type": "application/json"}
    
    message_content, user_id = format_message(message)
    
    data = {
        "content": message_content,
        "allowed_mentions": {"parse": ["users"], "users": [user_id] if user_id else []}
    }
    
    logging.info(f"Mengirim pesan ke channel {channel_id}: {data}")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 429:
        retry_after = response.json().get("retry_after", 0)
        SLOW_MODE_TRACKER[channel_id] = time.time() + retry_after
        logging.warning(f"Rate limit! Channel {channel_id} harus menunggu {retry_after} detik sebelum mengirim ulang.")
        return False, retry_after
    
    elif response.status_code in [200, 201]:
        slow_mode_delay = response.json().get("slowmode_delay", 0)
        if slow_mode_delay > 0:
            SLOW_MODE_TRACKER[channel_id] = time.time() + slow_mode_delay
            logging.info(f"Slow mode aktif {slow_mode_delay} detik untuk channel {channel_id}.")
        logging.info(f"Pesan berhasil dikirim ke channel {channel_id}.")
        return True, 0
    else:
        logging.error(f"Gagal mengirim pesan ke channel {channel_id}. Status: {response.status_code}, Respon: {response.text}")
        return False, 0

# Fungsi untuk mendapatkan daftar channel dari .env
def get_channels():
    config = load_config()
    channels = {key.replace("CHANNEL_", ""): value for key, value in config.items() if key.startswith("CHANNEL_")}
    logging.info(f"Daftar channel ditemukan: {list(channels.keys())}")
    return channels

# Fungsi untuk menambahkan channel baru ke .env
def add_channel():
    faucet_name = input("Masukkan Nama Faucet: ")  # Input baru untuk nama faucet
    channel_id = input("Masukkan Channel ID: ")
    message = input("Masukkan pesan yang ingin dikirim: ")
    with open(".env", "a") as f:
        f.write(f"\nCHANNEL_{channel_id}={message} # {faucet_name}")  # Menyimpan nama faucet sebagai komentar
    logging.info(f"Channel {channel_id} ({faucet_name}) dan pesan berhasil disimpan!")
    print("Channel dan pesan berhasil ditambahkan!")

# Fungsi untuk mengirim semua pesan
def send_all_messages():
    channels = get_channels()
    if not channels:
        logging.warning("Tidak ada channel yang tersimpan.")
        print("Tidak ada channel yang tersimpan.")
        return
    
    pending_channels = {}
    sent_channels = []
    
    # Kirim pesan ke setiap channel, hanya tunda jika terkena slow mode
    for channel_id, message in channels.items():
        success, wait_time = send_message(channel_id, message)
        if success:
            sent_channels.append(channel_id)
        if not success and wait_time > 0:
            pending_channels[channel_id] = (message, wait_time)
    
    logging.info(f"Pesan telah dikirim ke channel: {', '.join(sent_channels)}")
    print(f"Pesan telah dikirim ke channel: {', '.join(sent_channels)}")
    
    if pending_channels:
        logging.info("Channel yang terkena slow mode:")
        print("Channel yang terkena slow mode:")
        for channel_id, (_, wait_time) in pending_channels.items():
            logging.info(f" - {channel_id}: {wait_time} detik")
            print(f" - {channel_id}: {wait_time} detik")
    
    # Proses ulang hanya untuk channel yang terkena slow mode secara independen
    def process_pending():
        while pending_channels:
            for channel_id in list(pending_channels.keys()):
                message, wait_time = pending_channels[channel_id]
                time_to_wait = max(0, SLOW_MODE_TRACKER.get(channel_id, 0) - time.time())
                if time_to_wait > 0:
                    logging.info(f"Menunggu {time_to_wait} detik sebelum mengirim ulang ke channel {channel_id}.")
                    print(f"Menunggu {time_to_wait} detik sebelum mengirim ulang ke channel {channel_id}.")
                    time.sleep(time_to_wait)
                success, new_wait_time = send_message(channel_id, message)
                if success or new_wait_time == 0:
                    del pending_channels[channel_id]
                    sent_channels.append(channel_id)  # Tambahkan ke daftar berhasil dikirim
                    logging.info(f"Pesan akhirnya dikirim ke channel {channel_id}.")
        
        logging.info(f"Semua pesan berhasil dikirim ke channel: {', '.join(sent_channels)}")
        print(f"Semua pesan berhasil dikirim ke channel: {', '.join(sent_channels)}")

    slow_mode_thread = threading.Thread(target=process_pending)
    slow_mode_thread.start()

# Loop utama
try:
    while True:
        print("\nPilih opsi:")
        print("1. Claim faucet")
        print("2. Buat pesan baru untuk claim faucet")
        print("3. Keluar")  

        choice = input("Masukkan pilihan (1/2/3): ")

        if choice == "1":
            send_all_messages()
        elif choice == "2":
            add_channel()
            config = load_config()  # Reload config setelah menambah channel
            send_all_messages()  # Kirim pesan setelah channel baru ditambahkan
        elif choice == "3":
            print("Keluar dari program.")
            sys.exit(0)  # Hentikan program sepenuhnya
        else:
            print("Pilihan tidak valid, coba lagi.")

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")
    sys.exit(0)
