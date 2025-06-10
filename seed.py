from database import get_db_connection, init_db

def seed_data():
    """Mengisi database dengan data awal kursus."""
    conn = get_db_connection()
    c = conn.cursor()

    # Bersihkan data lama
    c.execute("DELETE FROM courses")
    conn.commit()

    # Data kursus
    courses = [
        ("Dasar Python", "Belajar sintaks dasar Python dan logika pemrograman", "Modul 1: Variabel\nModul 2: Percabangan\nModul 3: Perulangan"),
        ("Web Development", "Belajar HTML, CSS, dan dasar JavaScript", "Modul 1: HTML Dasar\nModul 2: CSS Styling\nModul 3: JavaScript Intro"),
        ("Machine Learning", "Pengantar Machine Learning dengan Python", "Modul 1: NumPy & Pandas\nModul 2: Sklearn\nModul 3: Model Supervised"),
    ]

    c.executemany("INSERT INTO courses (title, description, content) VALUES (?, ?, ?)", courses)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data kursus!")

if __name__ == "__main__":
    init_db()
    seed_data()
