# app/app.py

from flask import Flask
from flask_graphql import GraphQLView
from .schema import schema
from .models import init_db
import os

def create_app():
    app = Flask(__name__)
    
    # --- BAGIAN INI SANGAT PENTING ---
    # Buat folder data jika belum ada
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Folder 'data/' created!") # Tambahkan print statement untuk konfirmasi

    # Inisialisasi database saat aplikasi dimulai
    with app.app_context():
        init_db()
        print("Quiz database initialization completed.")

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    @app.route('/')
    def hello():
        return "Quiz Service is running! Access /graphql for the GraphQL API."

    return app

# Hanya jalankan server jika skrip ini dieksekusi langsung
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True) 