from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')

def get_db_connection():
    conn = sqlite3.connect('course/service/courses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return jsonify([dict(course) for course in courses])

@app.route('/api/courses', methods=['POST'])
def create_course():
    course_data = request.json
    if not course_data or not all(key in course_data for key in ['title', 'description', 'instructor']):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO courses (title, description, instructor) VALUES (?, ?, ?)',
        (course_data['title'], course_data['description'], course_data['instructor'])
    )
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': course_id, **course_data}), 201

@app.route('/api/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course_data = request.json
    if not course_data or not all(key in course_data for key in ['title', 'description', 'instructor']):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE courses SET title = ?, description = ?, instructor = ? WHERE id = ?',
        (course_data['title'], course_data['description'], course_data['instructor'], id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Course not found'}), 404

    return jsonify({'id': id, **course_data})

@app.route('/api/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Course not found'}), 404

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 