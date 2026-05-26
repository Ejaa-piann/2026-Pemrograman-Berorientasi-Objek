# Menulis teks ke file dengan mode 'w'
with open('log_file.txt', 'w') as file:
    file.write("Data Praktikum Selesai")

# Membaca dan mencetak isi file
with open('log_file.txt', 'r') as file:
    isi = file.read()
    print(isi)
