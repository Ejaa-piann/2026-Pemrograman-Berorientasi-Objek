import sqlite3
import os
from konfigurasi import DATABASE_NAME


class Database:

    def __init__(self):
        os.makedirs("data", exist_ok=True)

        self.conn = sqlite3.connect(
            DATABASE_NAME,
            check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            perusahaan TEXT,
            email TEXT,
            telepon TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS designer(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            spesialis TEXT,
            email TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS project(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_project TEXT NOT NULL,
            deskripsi TEXT,
            jenis TEXT,
            client_id INTEGER,
            designer_id INTEGER,
            deadline TEXT,
            budget REAL,
            status TEXT,
            category TEXT,
            image_path TEXT
        )
        """)
        # Migration: ensure category and image_path columns exist for older DBs
        try:
            self.cursor.execute("ALTER TABLE project ADD COLUMN category TEXT")
        except Exception:
            pass  # Column may already exist
        try:
            self.cursor.execute("ALTER TABLE project ADD COLUMN image_path TEXT")
        except Exception:
            pass  # Column may already exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS revision(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            revisi_ke INTEGER,
            catatan TEXT,
            tanggal TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            total REAL,
            dp REAL,
            sisa REAL,
            status TEXT
        )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()