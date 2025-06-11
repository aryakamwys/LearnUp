# 📘 Project Documentation – Microservices Architecture LearnUp


# 🧱 Tech Stack
### Backend Framework: Flask

### API Layer: GraphQL

### Database: SQLite

### Containerization: Docker, Docker Compose


🧩 Microservices Overview
1. 🔐 Authentication Service (User)
Description: Mengelola proses register, login, dan otentikasi pengguna.

🔗 Endpoints
Environment	Web URL	GraphQL Endpoint
Docker	http://localhost:5001	http://localhost:5001/graphql
Non-Docker	http://localhost:5000	http://localhost:5000/graphql

2. 🎓 Course Service
Description: Mengelola data kursus, materi, dan pengelolaan konten edukasi.

🔗 Endpoints
Environment	Web URL	GraphQL Endpoint
Docker	http://localhost:5002	http://localhost:5002/graphql
Non-Docker	http://localhost:5000	http://localhost:5000/graphql

2. 🎓 Loan Service
Description: Mpeminjaman buku.

🔗 Endpoints
Environment	Web URL	GraphQL Endpoint
Docker	http://localhost:5003	http://localhost:5003/graphql
Non-Docker	http://localhost:5000	http://localhost:5000/graphql

⚙️ Running the Project
🐳 Via Docker Compose
Build dan jalankan semua service:

docker-compose up --build

🔁 Otomatis menjalankan semua service (auth dan course) dengan port sesuai mapping di docker-compose.yml.

🧾 Catatan
Port Lokal untuk Non-Docker hanya menggunakan localhost:5000. Pastikan tidak menjalankan dua service secara bersamaan di port yang sama.
