from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from database import db_session, init_db
from graphene import Schema
from auth.schemas.auth_schema import AuthQuery, AuthMutation
from resolvers import Query, Mutation

app = Flask(__name__)
CORS(app)

# Combine auth and course schemas
class RootQuery(AuthQuery, Query):
    pass

class RootMutation(AuthMutation, Mutation):
    pass

schema = Schema(query=RootQuery, mutation=RootMutation)

# GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
