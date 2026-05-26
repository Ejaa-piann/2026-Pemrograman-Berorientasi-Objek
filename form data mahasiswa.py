#Data Mahasiswa
print("---Form Data Mahasiswa---")

nama= input("Masukkan Nama: ")
nim= input("Masukkan NIM: ")
kelas= input("Masukkan Kelas: ")

print("\n---Nihh Datamu---")
print(f"Hai Salam Kenal {nama}")
print(f"Jadi NIM kamu adalah {nim}")
print(f"Kelas kamu adalah {kelas}")

#Nilai Mahasiswa
print("\n---Nilai Mahasiswa---")

nilaitugas  = (float(input("Masukkan Nilai Tugas: ")))
nilaiuts    = (float(input("Masukkan Nilai UTS: ")))
nilaiuas    = (float(input("Masukkan Nilai UAS: ")))
nilaiakhir  = (nilaitugas+nilaiuts+nilaiuas) /3

print(f"\nHasil akhir nilaimu adalah: {nilaiakhir :.2f}")