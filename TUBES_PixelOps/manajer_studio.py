from datetime import datetime
from database import Database

class StudioManager:
    def __init__(self):
        self.db = Database()

    def tambah_client(self, nama, perusahaan, email, telepon):
        self.db.cursor.execute("INSERT INTO client (nama, perusahaan, email, telepon) VALUES (?, ?, ?, ?)",
            (nama, perusahaan, email, telepon)
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def hapus_client(self, client_id):
        self.db.cursor.execute("DELETE FROM client WHERE id = ?", (client_id,))
        self.db.conn.commit()

    def tampil_client(self):
        self.db.cursor.execute("SELECT * FROM client")
        return [dict(row) for row in self.db.cursor.fetchall()]

    def total_client(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM client")
        return self.db.cursor.fetchone()[0]

    def tambah_designer(self, nama, spesialis, email):
        # Prevent duplicate designers (same email)
        self.db.cursor.execute("SELECT id FROM designer WHERE email = ?", (email,))
        existing = self.db.cursor.fetchone()
        if existing:
            return existing['id']
        self.db.cursor.execute(
            "INSERT INTO designer (nama, spesialis, email) VALUES (?, ?, ?)",
            (nama, spesialis, email)
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def hapus_designer(self, designer_id):
        self.db.cursor.execute("DELETE FROM designer WHERE id = ?", (designer_id,))
        self.db.conn.commit()

    def tampil_designer(self):
        self.db.cursor.execute("SELECT * FROM designer")
        return [dict(row) for row in self.db.cursor.fetchall()]

    def total_designer(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM designer")
        return self.db.cursor.fetchone()[0]

    def tambah_project(self, nama, deskripsi, jenis, client_id, designer_id, deadline, budget, status="Progres", category=None, image_path=None):
        try:
            self.db.cursor.execute(
                "INSERT INTO project (nama_project, deskripsi, jenis, client_id, designer_id, deadline, budget, status, category, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (nama, deskripsi, jenis, client_id, designer_id, deadline, budget, status, category, image_path)
            )
        except Exception as e:
            # Fallback for older DB schema without category/image_path columns
            if "no column named" in str(e):
                self.db.cursor.execute(
                    "INSERT INTO project (nama_project, deskripsi, jenis, client_id, designer_id, deadline, budget, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (nama, deskripsi, jenis, client_id, designer_id, deadline, budget, status)
                )
            else:
                raise
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def tampil_project(self):
        query = """
        SELECT p.*, c.nama as client_nama, d.nama as designer_nama
        FROM project p
        LEFT JOIN client c ON p.client_id = c.id
        LEFT JOIN designer d ON p.designer_id = d.id
        ORDER BY p.id DESC
        """
        self.db.cursor.execute(query)
        return [dict(row) for row in self.db.cursor.fetchall()]

    def tampil_project_by_id(self, project_id):
        query = """
        SELECT p.*, c.nama as client_nama, d.nama as designer_nama
        FROM project p
        LEFT JOIN client c ON p.client_id = c.id
        LEFT JOIN designer d ON p.designer_id = d.id
        WHERE p.id = ?
        """
        self.db.cursor.execute(query, (project_id,))
        row = self.db.cursor.fetchone()
        return dict(row) if row else None

    def update_project(self, project_id, nama, deskripsi, jenis, client_id, designer_id, deadline, budget):
        self.db.cursor.execute("""
            UPDATE project SET nama_project=?, deskripsi=?, jenis=?, client_id=?,
            designer_id=?, deadline=?, budget=? WHERE id=?
        """, (nama, deskripsi, jenis, client_id, designer_id, deadline, budget, project_id))
        self.db.conn.commit()
        
    def update_status_project(self, project_id, status):
        self.db.cursor.execute("UPDATE project SET status = ? WHERE id = ?", (status, project_id))
        self.db.conn.commit()

    def hapus_project(self, project_id):
        self.db.cursor.execute("DELETE FROM project WHERE id = ?", (project_id,))
        self.db.cursor.execute("DELETE FROM revision WHERE project_id = ?", (project_id,))
        self.db.cursor.execute("DELETE FROM payment WHERE project_id = ?", (project_id,))
        self.db.conn.commit()

    def total_project(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM project")
        return self.db.cursor.fetchone()[0]

    def total_active_project(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM project WHERE status = 'Progres'")
        return self.db.cursor.fetchone()[0]

    def total_revisi_project(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM project WHERE status = 'Revisi'")
        return self.db.cursor.fetchone()[0]

    def total_selesai_project(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM project WHERE status = 'Selesai'")
        return self.db.cursor.fetchone()[0]

    def tambah_revisi(self, project_id, catatan):
        self.db.cursor.execute("SELECT MAX(revisi_ke) FROM revision WHERE project_id = ?", (project_id,))
        res = self.db.cursor.fetchone()[0]
        revisi_ke = 1 if res is None else res + 1
        
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.db.cursor.execute(
            "INSERT INTO revision (project_id, revisi_ke, catatan, tanggal) VALUES (?, ?, ?, ?)",
            (project_id, revisi_ke, catatan, tanggal)
        )
        # Auto update project status to Revisi
        self.update_status_project(project_id, "Revisi")
        self.db.conn.commit()

    def tampil_revisi(self):
        query = """
        SELECT r.*, p.nama_project
        FROM revision r
        JOIN project p ON r.project_id = p.id
        ORDER BY r.tanggal DESC
        """
        self.db.cursor.execute(query)
        return [dict(row) for row in self.db.cursor.fetchall()]

    def tampil_revisi_by_project(self, project_id):
        self.db.cursor.execute("SELECT * FROM revision WHERE project_id = ? ORDER BY revisi_ke DESC", (project_id,))
        return [dict(row) for row in self.db.cursor.fetchall()]

    def hapus_revisi(self, revisi_id):
        self.db.cursor.execute("DELETE FROM revision WHERE id = ?", (revisi_id,))
        self.db.conn.commit()

    def tambah_payment(self, project_id, total, dp):
        sisa = total - dp
        status = "Lunas" if sisa <= 0 else "DP" if dp > 0 else "Belum Bayar"
        
        self.db.cursor.execute(
            "INSERT INTO payment (project_id, total, dp, sisa, status) VALUES (?, ?, ?, ?, ?)",
            (project_id, total, dp, sisa, status)
        )
        self.db.conn.commit()

    def tampil_payment(self):
        query = """
        SELECT pay.*, p.nama_project, p.budget
        FROM payment pay
        JOIN project p ON pay.project_id = p.id
        ORDER BY pay.id DESC
        """
        self.db.cursor.execute(query)
        return [dict(row) for row in self.db.cursor.fetchall()]

    def hapus_payment(self, payment_id):
        self.db.cursor.execute("DELETE FROM payment WHERE id = ?", (payment_id,))
        self.db.conn.commit()

    def update_payment(self, payment_id, bayar_tambahan):
        self.db.cursor.execute("SELECT * FROM payment WHERE id = ?", (payment_id,))
        pay = self.db.cursor.fetchone()
        if pay:
            dp_baru = pay['dp'] + min(bayar_tambahan, pay['sisa'])
            sisa_baru = pay['total'] - dp_baru
            status = "Lunas" if sisa_baru <= 0 else "DP"
            self.db.cursor.execute(
                "UPDATE payment SET dp = ?, sisa = ?, status = ? WHERE id = ?",
                (dp_baru, sisa_baru, status, payment_id)
            )
            self.db.conn.commit()

    def total_revenue(self):
        self.db.cursor.execute("SELECT SUM(dp) FROM payment")
        res = self.db.cursor.fetchone()[0]
        return res if res else 0

    def total_piutang(self):
        self.db.cursor.execute("SELECT SUM(sisa) FROM payment")
        res = self.db.cursor.fetchone()[0]
        return res if res else 0

    def payment_status_counts(self):
        self.db.cursor.execute("SELECT status, COUNT(*) FROM payment GROUP BY status")
        stats = {'Lunas': 0, 'DP': 0, 'Belum Bayar': 0}
        for row in self.db.cursor.fetchall():
            stats[row[0]] = row[1]
        return stats
