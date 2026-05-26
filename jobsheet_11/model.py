# model.py
import datetime

class Transaksi:
    """Merepresentasikan satu entitas transaksi pengeluaran (Data Class)."""
    def __init__(self, deskripsi, jumlah, kategori, tanggal, id_transaksi = None):
        self.id = id_transaksi
        self.deskripsi = str(deskripsi) if deskripsi else "Tanpa Deskripsi"
        
        try:
            jumlah_float = float(jumlah)
            self.jumlah = jumlah_float if jumlah_float > 0 else 0.0
        except (ValueError, TypeError):
            self.jumlah = 0.0
            
        self.kategori = str(kategori) if kategori else "Lainnya"
        
        # Validasi Tanggal
        if isinstance(tanggal, datetime.date):
            self.tanggal = tanggal
        elif isinstance(tanggal, str):
            try:
                self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal = datetime.date.today()
        else:
            self.tanggal = datetime.date.today()

    def __repr__(self) -> str:
        # Format rupiah manual yang aman di Windows/Linux tanpa locale OS
        try:
            jml_str = f"{int(self.jumlah):,}".replace(",", ".")
        except:
            jml_str = f"{self.jumlah}"
        return f"Transaksi(ID: {self.id}, Tgl: {self.tanggal.strftime('%Y-%m-%d')}, Jml: Rp {jml_str}, Kat: '{self.kategori}', Desc: '{self.deskripsi}')"

    def to_dict(self) -> dict:
        return {
            "deskripsi": self.deskripsi,
            "jumlah": self.jumlah,
            "kategori": self.kategori,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }