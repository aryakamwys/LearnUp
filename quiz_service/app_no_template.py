import os
from flask import Flask, request, jsonify
from database import init_db, db_session
from models.quiz import Quiz
from models.question import Question
from models.option import Option
from models.quiz_result import QuizResult

# Initialize the database
init_db()

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "Quiz Service - LearnUp",
        "status": "Active",
        "port": 5004,
        "endpoints": {
            "GET /api/quizzes": "Daftar semua quiz",
            "POST /api/quizzes": "Membuat quiz baru",
            "GET /api/quizzes/{id}/questions": "Pertanyaan dalam quiz",
            "POST /api/quizzes/{id}/questions": "Menambah pertanyaan",
            "POST /api/questions/{id}/options": "Menambah pilihan jawaban"
        }
    })

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = db_session.query(Quiz).filter_by(is_active=1).all()
    return jsonify([{
        'id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'time_limit': quiz.time_limit,
        'passing_score': quiz.passing_score
    } for quiz in quizzes])

@app.route('/api/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    quiz = Quiz(
        title=data.get('title'),
        description=data.get('description'),
        time_limit=data.get('time_limit', 0),
        passing_score=data.get('passing_score', 70)
    )
    db_session.add(quiz)
    db_session.commit()
    return jsonify({'id': quiz.id, 'message': 'Quiz created successfully'})

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    questions = db_session.query(Question).filter_by(quiz_id=quiz_id).order_by(Question.order_index).all()
    return jsonify([{
        'id': q.id,
        'question_text': q.question_text,
        'question_type': q.question_type,
        'points': q.points
    } for q in questions])

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
def create_question(quiz_id):
    data = request.get_json()
    question = Question(
        quiz_id=quiz_id,
        question_text=data.get('question_text'),
        question_type=data.get('question_type', 'multiple_choice'),
        points=data.get('points', 1)
    )
    db_session.add(question)
    db_session.commit()
    return jsonify({'id': question.id, 'message': 'Question created successfully'})

@app.route('/api/questions/<int:question_id>/options', methods=['POST'])
def create_option(question_id):
    data = request.get_json()
    option = Option(
        question_id=question_id,
        option_text=data.get('option_text'),
        is_correct=data.get('is_correct', False)
    )
    db_session.add(option)
    db_session.commit()
    return jsonify({'id': option.id, 'message': 'Option created successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True) 