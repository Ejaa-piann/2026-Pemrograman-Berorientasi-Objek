# Algoritma CariNilaiTerbesar

# Deklarasi variabel
# bilangan1, bilangan2, nilai_terbesar : integer

# Input bilangan pertama
bilangan1 = int(input("Masukkan bilangan pertama: "))

# Input bilangan kedua
bilangan2 = int(input("Masukkan bilangan kedua: "))

# Proses mencari nilai terbesar
if bilangan1 > bilangan2:
    nilai_terbesar = bilangan1
else:
    nilai_terbesar = bilangan2

# Output nilai terbesar
print("Nilai terbesar adalah", nilai_terbesar)
