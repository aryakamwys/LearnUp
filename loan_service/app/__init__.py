from flask import Flask, render_template
from flask_graphql import GraphQLView
from .schema import schema
from .models import init_db

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

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
