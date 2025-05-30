import sqlite3

# Buat dan koneksi ke database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Buat tabel user
c.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Buat tabel konsultasi
c.execute('''
    CREATE TABLE IF NOT EXISTS konsultasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        pertanyaan TEXT NOT NULL,
        waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database berhasil dibuat!")
