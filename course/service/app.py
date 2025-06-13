import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BASE_DIR)

IN_DOCKER = os.environ.get('IN_DOCKER') == '1'

if IN_DOCKER:
    STATIC_FOLDER = '/app/static'
    TEMPLATE_FOLDER = '/app/templates'
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    sys.path.append(BASE_DIR)
    STATIC_FOLDER = os.path.join(BASE_DIR, 'course', 'static')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'course', 'templates')

from flask import Flask, render_template
from graphql_server.flask import GraphQLView
from graphene import Schema
from resolvers import Query, Mutation


app = Flask(
    __name__,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER
)

print("TEMPLATE FOLDER:", TEMPLATE_FOLDER)
print("INDEX EXISTS?", os.path.exists(os.path.join(TEMPLATE_FOLDER, 'index.html')))

schema = Schema(query=Query, mutation=Mutation)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/course.html')
def course_detail():
    return render_template('course.html')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
