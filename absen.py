from datetime import datetime, timedelta
import requests
import os
import time
import random

# Ambil data login dari GitHub Secrets
username = os.environ.get("ABSEN_USER")
password = os.environ.get("ABSEN_PASS")

# Ambil waktu sekarang (UTC) dan ubah ke WIB
now_utc = datetime.utcnow()
now = now_utc + timedelta(hours=7)

hari = now.strftime("%A")  # contoh: Monday
tanggal = now.strftime("%Y-%m-%d")
jam = now.strftime("%H:%M")

print("=== Menjalankan script absen otomatis ===")
print("Waktu sekarang (WIB):", now.strftime("%Y-%m-%d %H:%M:%S"))
print("Hari:", hari)
print("Username:", username)
print("----------------------------------------")

# 1️⃣ Cek apakah hari Sabtu/Minggu
if hari in ["Saturday", "Sunday"]:
    print("Hari ini libur (Sabtu/Minggu) — tidak absen.")
    exit()

# 2️⃣ Cek apakah hari libur nasional via API
try:
    response = requests.get("https://api-harilibur.vercel.app/api", timeout=10)
    holidays = response.json()
    daftar_libur = [h["holiday_date"] for h in holidays]
    if tanggal in daftar_libur:
        print(f"Hari ini ({tanggal}) adalah hari libur nasional — tidak absen.")
        exit()
except Exception as e:
    print("Gagal cek hari libur, lanjutkan saja:", e)

# 3️⃣ Tentukan jenis absen berdasarkan jam WIB
if jam == "06:10":
    jenis = "Absen Pagi"
elif jam == "12:10":
    jenis = "Absen Siang"
elif hari == "Friday" and jam == "16:40":
    jenis = "Absen Sore Jumat"
elif jam == "16:10":
    jenis = "Absen Sore"
else:
    jenis = "Tidak ada absen saat ini"

print(f"Jenis absen: {jenis}")

# 4️⃣ Jalankan proses absen jika waktunya sesuai
if "Absen" in jenis:
    # Tambahkan delay acak 3–5 detik sebelum submit
    delay = random.uniform(3, 5)
    print(f"Menunggu {delay:.2f} detik sebelum mengirim absen...")
    time.sleep(delay)

    print("👉 Menjalankan proses absen...")
    # TODO: tambahkan logika login ke website absen kamu di sini
    # Contoh:
    # response = requests.post("https://url-absen", data={"user": username, "pass": password})
    # print("Hasil:", response.status_code, response.text)

else:
    print("⏸️ Tidak perlu absen sekarang.")

print("=== Selesai ===")
