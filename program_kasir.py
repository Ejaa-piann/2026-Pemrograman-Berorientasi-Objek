# Deskripsi: Program kasir interaktif dengan logika diskon 10% jika pembelian > Rp 500.000.

# 2. Rancang Proses Input
print("--- Program Kasir Sederhana ---")
total_pembelian = float(input("Masukkan Total Pembelian Pelanggan (Rp): "))

# 3. Implementasikan Logika Percabangan (if-else)
batas_diskon = 500000
persentase_diskon = 0.10 # 10%

if total_pembelian > batas_diskon:
    # Kondisi if: Jika pembelian di atas 500.000, hitung diskon.
    diskon = total_pembelian * persentase_diskon
else:
    # Kondisi else: Jika tidak, diskon adalah 0.
    diskon = 0

# Menghitung total bayar akhir
total_bayar = total_pembelian - diskon

# 4. Sajikan Struk Pembayaran

print("\n===============================")
print("      STRUK PEMBAYARAN")
print("===============================")
print(f"Total Pembelian : Rp {total_pembelian:,.0f}")
print(f"Diskon (10%)    : Rp {diskon:,.0f}")
print("-------------------------------")
print(f"Total Bayar     : Rp {total_bayar:,.0f}")
print("===============================")
print("  Terima kasih telah berbelanja! ")
print("===============================")