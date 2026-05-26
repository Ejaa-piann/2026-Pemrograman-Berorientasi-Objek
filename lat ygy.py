# Membuat dictionary 
kota = {
    0: "Jakarta",
    1: "Bandung",
    2: "Surabaya"
}
# Cetak dictionary
print("Dictionary kota awal:")
print(kota)

# Tambahkan elemen “Banten” ke kota
kota[3] = "Banten"

# Cetak dictionary setelah penambahan
print("\nDictionary kota setelah menambahkan 'Banten':")
print(kota)

# Hitung jumlah elemen sekarang pada dictionary kota
jumlah_elemen = len(kota)
print(f"\nJumlah elemen sekarang pada dictionary kota: {jumlah_elemen}")