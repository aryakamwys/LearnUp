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
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Service - LearnUp</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; text-align: center; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; font-family: monospace; }
            .btn { background: #1a73e8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Quiz Service</h1>
            <p>Microservice untuk mengelola quiz dan evaluasi pembelajaran</p>
            
            <h2>🔗 API Endpoints</h2>
            <div class="endpoint">
                <strong>GET /api/quizzes</strong> - Daftar semua quiz
                <a href="/api/quizzes" class="btn">Test</a>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/quizzes</strong> - Membuat quiz baru
            </div>
            
            <div class="endpoint">
                <strong>GET /api/quizzes/{id}/questions</strong> - Pertanyaan dalam quiz
            </div>
            
            <div class="endpoint">
                <strong>POST /api/quizzes/{id}/questions</strong> - Menambah pertanyaan
            </div>
            
            <div class="endpoint">
                <strong>POST /api/questions/{id}/options</strong> - Menambah pilihan jawaban
            </div>
            
            <h2>📊 Status</h2>
            <p>✅ Service berjalan di port 5004</p>
        </div>
    </body>
    </html>
    '''

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