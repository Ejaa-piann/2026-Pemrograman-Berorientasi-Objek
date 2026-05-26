# Membuat dictionary mahasiswa dengan kunci: nama, prodi, pembimbing
mahasiswa = {
    "nama": "Ahmad Fauzi",
    "prodi": "Teknik Informatika",
    "pembimbing": "Dr. Siti Nurhaliza"
}
# Menampilkan hasil dictionary
print("Data Mahasiswa:")
for key, value in mahasiswa.items():
    print(f"{key.capitalize()}: {value}")