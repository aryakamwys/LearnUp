from flask import Flask, render_template
from flask_graphql import GraphQLView
from .schema import schema
from .models import init_db
import requests

def create_app():
    app = Flask(__name__)
    
    # Initialize database
    init_db()
    print("Database initialized successfully!")

    # Add GraphQL endpoint
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    def fetch_users():
        try:
            resp = requests.post(
                "http://localhost:5001/graphql",
                json={"query": "query { allUsers { id name } }"}
            )
            data = resp.json()
            return data['data']['allUsers']
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def fetch_courses():
        try:
            resp = requests.post(
                "http://localhost:5002/graphql",
                json={"query": "query { allCourses { id title } }"}
            )
            data = resp.json()
            return data['data']['allCourses']
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []

    @app.route('/')
    def index():
        users = fetch_users()
        courses = fetch_courses()
        return render_template('index.html', users=users, courses=courses)

    return app
