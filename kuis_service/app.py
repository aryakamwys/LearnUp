import os
from flask import Flask, render_template, request, jsonify
from graphql_server.flask import GraphQLView
from graphene import Schema
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import resolver and database init
from resolver import Query, Mutation
from database import init_db

# Initialize the database
init_db()

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

schema = Schema(query=Query, mutation=Mutation)

@app.route('/')
def index():
    return render_template('index.html')

# Add GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # enable GraphiQL GUI
    )
)

# REST API endpoints for backward compatibility (optional, can be removed if only GraphQL is desired)
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes_rest():
    from models.quiz import Quiz
    from database import db_session
    quizzes = db_session.query(Quiz).filter_by(is_active=True).all()
    return jsonify([
        {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'time_limit': quiz.time_limit,
            'passing_score': quiz.passing_score
        } for quiz in quizzes
    ])

@app.route('/api/quizzes', methods=['POST'])
def create_quiz_rest():
    from models.quiz import Quiz
    from database import db_session
    data = request.get_json()
    quiz = Quiz(
        title=data.get('title'),
        description=data.get('description'),
        time_limit=data.get('time_limit', 0),
        passing_score=data.get('passing_score', 70)
    )
    db_session.add(quiz)
    db_session.commit()
    return jsonify({'id': quiz.id, 'message': 'Quiz created successfully'}), 201

# Add routes for updating and deleting quizzes (REST for example)
@app.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz_rest(quiz_id):
    from models.quiz import Quiz
    from database import db_session
    quiz = db_session.query(Quiz).filter_by(id=quiz_id, is_active=True).first()
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    data = request.get_json()
    quiz.title = data.get('title', quiz.title)
    quiz.description = data.get('description', quiz.description)
    quiz.time_limit = data.get('time_limit', quiz.time_limit)
    quiz.passing_score = data.get('passing_score', quiz.passing_score)
    db_session.commit()
    return jsonify({'id': quiz.id, 'message': 'Quiz updated successfully'}), 200

@app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz_rest(quiz_id):
    from models.quiz import Quiz
    from database import db_session
    quiz = db_session.query(Quiz).filter_by(id=quiz_id, is_active=True).first()
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    quiz.is_active = False # Soft delete
    db_session.commit()
    return jsonify({'message': 'Quiz deleted successfully (soft delete)'}), 200

# User authentication simulation (for demonstration purposes)
# In a real microservice architecture, this would typically involve an auth service
def require_role(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # In a real app, you would validate a token here
            # For this example, let's assume a simple header check or env var
            user_role = request.headers.get('X-User-Role', 'user') # Default to 'user'

            if role == 'admin' and user_role != 'admin':
                return jsonify({'message': 'Unauthorized: Admin access required'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example of protecting an endpoint with role
@app.route('/admin/quizzes', methods=['POST'])
@require_role('admin')
def create_quiz_admin():
    # This endpoint would be protected by the admin role decorator
    # You can reuse create_quiz_rest logic or call GraphQL mutation
    return create_quiz_rest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True) 