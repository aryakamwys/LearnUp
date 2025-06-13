import os
from flask import Flask, render_template, request, redirect, session, url_for
from graphql_server.flask import GraphQLView
from graphene import Schema
import requests
from werkzeug.security import check_password_hash

from resolver import Query, Mutation
from database import init_db, db_session
from models.user import User

# Initialize the database
init_db()

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)
app.secret_key = 'learnup-super-secret-key-2024'

schema = Schema(query=Query, mutation=Mutation)

@app.route('/')
def index():
    return render_template('index.html')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # enable GraphiQL GUI
    )
)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db_session.query(User).filter_by(username=username).first()
    if username == 'admin' and user and check_password_hash(user.password_hash, password):
        session['username'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    elif user and check_password_hash(user.password_hash, password):
        session['username'] = username
        session['user_id'] = user.id
        return redirect(url_for('user_dashboard'))
    else:
        # Jika gagal login, tampilkan pesan error di halaman index
        return render_template('index.html', error='Username atau password salah!')

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('index'))
    # Fetch all courses
    courses = requests.post('http://course-service:5000/graphql', json={'query': 'query { allCourses { id title description } }'}).json()['data']['allCourses']
    # Fetch all loans
    loans = requests.post('http://loan-service:5000/graphql', json={'query': 'query { allLoans { id userId courseId loanDate isReturned } }'}).json()['data']['allLoans']
    # Fetch all quizzes
    quizzes = requests.post('http://quiz-service:5000/graphql', json={'query': 'query { allQuizzes { id title description } }'}).json()['data']['allQuizzes']
    return render_template('admin_dashboard.html', courses=courses, loans=loans, quizzes=quizzes)

@app.route('/dashboard')
def user_dashboard():
    if 'username' not in session or session['username'] == 'admin':
        return redirect(url_for('index'))
    # Fetch courses
    courses = requests.post('http://course-service:5000/graphql', json={'query': 'query { allCourses { id title description } }'}).json()['data']['allCourses']
    # Fetch quizzes
    quizzes = requests.post('http://quiz-service:5000/graphql', json={'query': 'query { allQuizzes { id title description } }'}).json()['data']['allQuizzes']
    # Fetch loans for this user (optional)
    user_id = session.get('user_id')
    loans = requests.post('http://loan-service:5000/graphql', json={'query': f'query {{ allLoans {{ id userId courseId loanDate isReturned }} }}'}).json()['data']['allLoans']
    user_loans = [l for l in loans if str(l['userId']) == str(user_id)]
    return render_template('user_dashboard.html', courses=courses, quizzes=quizzes, loans=user_loans)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
