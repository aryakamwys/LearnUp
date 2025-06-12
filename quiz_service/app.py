import os
import json
from flask import Flask, render_template, request, jsonify
from graphene import Schema
from graphql import graphql_sync

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

@app.route('/graphql', methods=['GET', 'POST'])
def graphql():
    if request.method == 'GET':
        # Return GraphiQL interface
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>GraphiQL</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/2.4.7/graphiql.min.css" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.production.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.production.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/2.4.7/graphiql.min.js"></script>
        </head>
        <body style="margin: 0;">
            <div id="graphiql" style="height: 100vh;"></div>
            <script>
                ReactDOM.render(
                    React.createElement(GraphiQL, {
                        fetcher: GraphiQL.createFetcher({
                            url: '/graphql',
                        }),
                    }),
                    document.getElementById('graphiql'),
                );
            </script>
        </body>
        </html>
        '''
    
    # Handle POST requests (GraphQL queries)
    data = request.get_json()
    query = data.get('query')
    variables = data.get('variables')
    
    if not query:
        return jsonify({'errors': [{'message': 'No query provided'}]}), 400
    
    try:
        result = graphql_sync(schema.graphql_schema, query, variable_values=variables)
        return jsonify(result)
    except Exception as e:
        return jsonify({'errors': [{'message': str(e)}]}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True) 