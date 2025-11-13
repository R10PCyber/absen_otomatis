import datetime
import os

print("Username:", os.environ.get("ABSEN_USER"))
print("Password:", os.environ.get("ABSEN_PASS"))

# Contoh sederhana (belum login ke web)
print("Script absen otomatis dijalankan pada:", datetime.datetime.now())
