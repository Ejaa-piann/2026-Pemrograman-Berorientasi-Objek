# Daftar harga barang dalam keranjang
daftar_harga = [15000, 5000, 20000, 50000, 2500]

# Variabel awal untuk menyimpan total
total_belanja = 0

print("Menghitung total belanja...")

for harga in daftar_harga:
    total_belanja += harga  # Menambahkan harga barang saat ini ke total
    print(f"Menambahkan item seharga: Rp {harga}")

# Menampilkan hasil akhir
print("-" * 30)
print(f"Total yang harus dibayar: Rp {total_belanja}")