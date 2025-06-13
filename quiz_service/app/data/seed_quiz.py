import os
from sqlalchemy.orm import Session
from quiz_service.app.models import Quiz, QuizQuestion, SessionLocal, init_db

# Inisialisasi DB dan session
init_db()
session = SessionLocal()

# Data dummy quiz dan soal
quizzes = [
    Quiz(title='Quiz Python Dasar', description='Quiz untuk materi Python dasar', course_id=1),
    Quiz(title='Quiz Web Development', description='Quiz untuk materi Web Development', course_id=2),
    Quiz(title='Quiz Machine Learning', description='Quiz untuk materi Machine Learning', course_id=3),
]

questions = [
    # Quiz 1
    QuizQuestion(quiz=quizzes[0], question_text='Apa output dari print(2+3)?', option_a='5', option_b='23', option_c='2+3', option_d='Error', correct_answer='A', points=1),
    QuizQuestion(quiz=quizzes[0], question_text='Tipe data dari 3.14 di Python adalah?', option_a='int', option_b='float', option_c='str', option_d='bool', correct_answer='B', points=1),
    # Quiz 2
    QuizQuestion(quiz=quizzes[1], question_text='Tag HTML untuk heading terbesar adalah?', option_a='<h1>', option_b='<h6>', option_c='<p>', option_d='<title>', correct_answer='A', points=1),
    QuizQuestion(quiz=quizzes[1], question_text='CSS digunakan untuk?', option_a='Struktur', option_b='Logika', option_c='Styling', option_d='Database', correct_answer='C', points=1),
    # Quiz 3
    QuizQuestion(quiz=quizzes[2], question_text='Library Python untuk machine learning adalah?', option_a='Flask', option_b='NumPy', option_c='Scikit-learn', option_d='Django', correct_answer='C', points=1),
    QuizQuestion(quiz=quizzes[2], question_text='Supervised learning artinya?', option_a='Belajar dengan label', option_b='Belajar tanpa label', option_c='Belajar sendiri', option_d='Belajar kelompok', correct_answer='A', points=1),
]

# Hapus data lama
session.query(QuizQuestion).delete()
session.query(Quiz).delete()
session.commit()

# Tambah data baru
for quiz in quizzes:
    session.add(quiz)
session.commit()
for q in questions:
    session.add(q)
session.commit()

print('Dummy quiz dan soal berhasil di-seed!')
session.close() 