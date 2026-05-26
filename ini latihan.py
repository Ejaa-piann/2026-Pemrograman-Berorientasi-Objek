def hitung_rata(daftar_nilai):
    if not daftar_nilai:
        return 0
    return sum(daftar_nilai) / len(daftar_nilai)


def nilai_huruf(rata):
    if rata >= 85:
        return "A"
    elif rata >= 70:
        return "B"
    elif rata >= 60:
        return "C"
    elif rata >= 50:
        return "D"
    else:
        return "E"


def cek_kelulusan(rata, batas_lulus=70):
    if rata >= batas_lulus:
        return "Lulus"
    else:
        return "Tidak Lulus"


def buat_laporan_mahasiswa(nama, nim, daftar_nilai):
    rata = hitung_rata(daftar_nilai)
    huruf = nilai_huruf(rata)
    status = cek_kelulusan(rata)

    laporan = (
        "=== Laporan Nilai Mahasiswa ===\n"
        f"Nama        : {nama}\n"
        f"NIM         : {nim}\n"
        f"Daftar Nilai: {', '.join(str(n) for n in daftar_nilai)}\n"
        f"Rata-rata   : {rata:.2f}\n"
        f"Nilai Huruf : {huruf}\n"
        f"Status      : {status}\n"
    )
    return laporan


# ===== BONUS =====

def tambah_nilai(daftar_nilai, nilai_baru):
    daftar_nilai.append(nilai_baru)
    return daftar_nilai


def rata_rata_kelas(data_mahasiswa):
    total_nilai = 0
    jumlah_nilai = 0
    for m in data_mahasiswa:
        total_nilai += sum(m["nilai"])
        jumlah_nilai += len(m["nilai"])
    if jumlah_nilai == 0:
        return 0
    return total_nilai / jumlah_nilai


# ===== CONTOH PEMAKAIAN =====

mhs1 = {"nama": "Alvian", "nim": "12345", "nilai": [80, 75, 90]}
mhs2 = {"nama": "Budi", "nim": "23456", "nilai": [60, 70, 65]}

print(buat_laporan_mahasiswa(mhs1["nama"], mhs1["nim"], mhs1["nilai"]))
print(buat_laporan_mahasiswa(mhs2["nama"], mhs2["nim"], mhs2["nilai"]))

tambah_nilai(mhs1["nilai"], 85)
print("Nilai Faiz setelah ditambah:", mhs1["nilai"])

data_kelas = [mhs1, mhs2]
print("Rata-rata kelas:", rata_rata_kelas(data_kelas))
