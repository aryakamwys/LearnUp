# 🚀 Cara Menjalankan Quiz Service

## 📋 Langkah 1: Buka Terminal
```bash
cd "D:\codingan herjun\iae_tubes-Quiz_Herjuno\quiz_service"
```

## 📦 Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## 🗄️ Langkah 3: Hapus Database Lama (jika ada)
```bash
# Di PowerShell:
Remove-Item -Recurse -Force data

# Atau di Command Prompt:
rmdir /s /q data
```

## ▶️ Langkah 4: Jalankan Service
```bash
python app_simple.py
```

## ✅ Hasil Sukses
```
📂 DB path: D:\codingan herjun\iae_tubes-Quiz_Herjuno\quiz_service\data\quiz.db
📥 Importing Quiz models...
📐 Creating all tables...
✅ Database initialized and tables created.
 * Serving Flask app 'app_simple'
 * Debug mode: on
 * Running on http://0.0.0.0:5004
```

## 🌐 Akses Service
- **Web:** http://localhost:5004
- **API:** http://localhost:5004/api/quizzes

## 🔧 Jika Error

### Error: "No module named 'flask'"
```bash
pip install flask==2.0.1
```

### Error: "Port already in use"
Ganti port di `app_simple.py`:
```python
app.run(host='0.0.0.0', port=5005, debug=True)
```

### Error: "Database locked"
```bash
Remove-Item -Recurse -Force data
python app_simple.py
```

## 🎯 Test API
```bash
# Lihat daftar quiz
curl http://localhost:5004/api/quizzes

# Buat quiz baru
curl -X POST http://localhost:5004/api/quizzes -H "Content-Type: application/json" -d "{\"title\":\"Quiz Test\",\"description\":\"Quiz untuk testing\"}"
``` 