#Menghitung luas dan keliling persegi panjang 

# 2. Inisialisasi Variabel Statis
# Nilai panjang dan lebar.
print("--- Kalkulator Luas & Keliling Persegi Panjang ---")
panjang = float(input("Masukkan nilai panjang: "))
lebar = float(input("Masukkan nilai lebar: "))

# 3. Implementasikan Proses Perhitungan
# Menghitung luas dan keliling menggunakan operator aritmatika.
luas = panjang * lebar
keliling = 2 * (panjang + lebar)

# 4. Tampilkan Hasil Kalkulasi
# Mencetak hasil perhitungan
print("--- Hasil Perhitungan Geometri ---")
print(f"Nilai Panjang  : {panjang} unit")
print(f"Nilai Lebar    : {lebar} unit")
print("------------------------------------")
print(f"Luas Persegi Panjang     : {luas} unit persegi")
print(f"Keliling Persegi Panjang : {keliling} unit")
print("------------------------------------")