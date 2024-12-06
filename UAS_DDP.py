from prettytable import PrettyTable
import time
import pwinput

# Data user 
user = {
    'Rini': {'password': '123', 'type': 'Member Biasa'},
    'Wulan': {'password': '0312', 'type': 'Member VIP'}
}

# Data barang yang tersedia di toko berdasarkan waktu
barang_pagi = [
    {'nama': 'Baju', 'harga': 50},
    {'nama': 'Sepatu', 'harga': 80},
    {'nama': 'Sandal', 'harga': 30},
    {'nama': 'Celana', 'harga': 70},
    {'nama': 'Rok tutu', 'harga': 50},
    {'nama': 'Sweater', 'harga': 100},
    {'nama': 'Hoodie', 'harga': 85}
]

barang_siang = [
    {'nama': 'Topi', 'harga': 60},
    {'nama': 'Tas', 'harga': 90},
    {'nama' : 'Kacamata', 'harga': 40},
    {'nama': 'Sandal', 'harga': 45},
    {'nama': 'Dompet', 'harga': 50},
    {'nama': 'Totebag', 'harga': 65},
    {'nama': 'Gelang', 'harga': 20}
]

barang_malam = [
    {'nama': 'Jam', 'harga': 100},
    {'nama': 'Kacamata', 'harga': 120},
    {'nama': 'Tas', 'harga': 50},
    {'nama': 'Cincin', 'harga': 10},
    {'nama': 'Belt', 'harga': 18},
    {'nama': 'Anting', 'harga': 38},
    {'nama': 'Parfum', 'harga': 88},
    {'nama': 'Syal', 'harga': 65},
    {'nama': 'Pita', 'harga': 55}
]

# Data voucher
voucher = {
    'VOUCHER10': {'diskon': 10, 'status': 'Aktif'},
    'VOUCHER15': {'diskon': 15, 'status': 'Aktif'},
    'VOUCHER20': {'diskon': 20, 'status': 'Aktif'}
}

# Data Saldo
saldo = {
    'Rini': {'saldo': 100, 'status': 'Aktif'},
    'Wulan': {'saldo': 300, 'status': 'Aktif'}
}

# Fungsi login
def login():
    print()
    print("=" * 6 + "Selamat Datang di Toko Online Fashion Riwuu'z" + "=" * 6)
    attempts = 0
    while attempts < 3:
        print()
        nama = input("Masukkan nama anda: ")
        password = pwinput.pwinput("Masukkan password anda: ")
        if nama in user and user[nama]['password'] == password:
            print(f"Selamat datang, {nama}! Anda Login sebagai {user[nama]['type']} ^-^")
            return nama
        else:
            print()
            attempts += 1
            print(f"Login gagal! Sisa percobaan: {3 - attempts}")
            if attempts == 3:
                print()
                print("Akun terkunci setelah 3 kali percobaan salah.")
                return None

# Fungsi Lihat Barang
def lihat_barang(waktu):
    if waktu == 'pagi':
        return barang_pagi
    elif waktu == 'siang':
        return barang_siang
    elif waktu == 'malam':
        return barang_malam
    else:
        return []

# Fungsi Tampilkan Barang
def tampilkan_barang(barang):
    table = PrettyTable()
    table.field_names = ["No", "Nama Barang", "Harga"]
    for index, item in enumerate(barang, 1):
        table.add_row([index, item['nama'], item['harga']])
    print(table)

# Fungsi Tambah Gems
def tambah_gems(saldo, jumlah, username):
    if user[username]['type'] == 'Member Biasa' and saldo + jumlah > 800:
        print("Sebagai Member Biasa, saldo Anda tidak bisa melebihi 800 Gems.")
        return saldo
    saldo += jumlah
    print(f"Saldo Anda berhasil ditambahkan.\nGems Anda saat ini: {saldo}")
    return saldo

# Fungsi Cek Saldo
def cek_saldo(username):
    print(f"Saldo Anda saat ini: {saldo[username]['saldo']} Gems")

# Fungsi Beli Barang
def beli_barang(username):
    current_time = time.localtime().tm_hour
    if 6 <= current_time < 12:
        waktu = 'pagi'
    elif 12 <= current_time < 18:
        waktu = 'siang'
    else:
        waktu = 'malam'

    barang = lihat_barang(waktu)
    print(f"\nBarang yang tersedia pada waktu {waktu}:")
    tampilkan_barang(barang)

    # Pilih barang yang akan dibeli
    while True:
        try:
            pilihan = int(input("Pilih nomor barang yang ingin dibeli (0 untuk batal): "))
            if pilihan == 0:
                print("Pembelian dibatalkan. Terimakasih ^-^")
                return saldo[username]['saldo']
            elif 1 <= pilihan <= len(barang):
                item_pilihan = barang[pilihan - 1]
                harga_barang = item_pilihan['harga']
                print(f"Anda memilih {item_pilihan['nama']} dengan harga {harga_barang}")
                break
            else:
                print("Pilihan barang tidak valid. Coba lagi.")
        except ValueError:
            print("Masukkan nomor yang valid.")

    if saldo[username]['saldo'] < harga_barang:
        print("Mohon maaf saldo Anda tidak cukup untuk membeli barang ini.")
        return saldo[username]['saldo']

    voucher_code = input("\nMasukkan kode voucher (kosongkan jika tidak ingin menggunakan voucher): ").upper()
    diskon = 0
    if voucher_code in voucher:
        if voucher[voucher_code]['status'] == 'Aktif':
            diskon = voucher[voucher_code]['diskon']
            print(f"Voucher {voucher_code} digunakan! Diskon: {diskon}%")
            voucher[voucher_code]['status'] = 'Tidak Aktif'  # Voucher hanya bisa digunakan sekali
        else:
            print("Voucher sudah digunakan atau tidak valid.")
    else:
        print("Voucher tidak ditemukan.")

    harga_diskon = harga_barang - (harga_barang * diskon / 100)
    saldo[username]['saldo'] -= harga_diskon
    print(f"Total harga : {harga_diskon}. Saldo Anda sekarang: {saldo[username]['saldo']}")
    print("Terimakasih telah berbelanja di toko kami!! ^-^.") 
    return saldo[username]['saldo']

# Program utama
def main():
    username = login()
    if username:
        while True:
            print("\nMenu:")
            print("1. Beli Barang")
            print("2. Cek Gems")
            print("3. Tambah Gems")
            print("4. Keluar")
            pilihan = input("Pilih menu (1/2/3/4): ")

            if pilihan == '1':
                saldo[username]['saldo'] = beli_barang(username)
            elif pilihan == '2':
                cek_saldo(username)
            elif pilihan == '3':
                while True:
                    try:
                        print()
                        jumlah = int(input("Masukkan jumlah gems yang ingin ditambahkan: "))
                        if jumlah > 0:
                            saldo[username]['saldo'] = tambah_gems(saldo[username]['saldo'], jumlah, username)
                            break
                        else:
                            print("Jumlah harus lebih dari 0.")
                    except ValueError:
                        print("Masukkan jumlah yang valid.")
            elif pilihan == '4':
                print("Terima kasih sudah berbelanja! ^-^")
                break
            else:
                print("Pilihan menu tidak valid.")
    else:
        print("Akses dibatasi karena kesalahan login.")

main()
