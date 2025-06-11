import os
from flask import Flask, render_template
from graphql_server.flask import GraphQLView
from graphene import Schema

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

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # enable GraphiQL GUI
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
