from graphene import ObjectType, String, Int, Field, List, Mutation
from database import db_session
import sqlite3

class Course(ObjectType):
    id = Int()
    title = String()
    description = String()
    content = String()
    created_at = String()
    updated_at = String()

class Query(ObjectType):
    courses = List(Course)
    course = Field(Course, id=Int())

    def resolve_courses(self, info):
        conn = sqlite3.connect('courses.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        conn.close()
        return [
            Course(
                id=course['id'],
                title=course['title'],
                description=course['description'],
                content=course['content'],
                created_at=course['created_at'],
                updated_at=course['updated_at']
            ) for course in courses
        ]

    def resolve_course(self, info, id):
        conn = sqlite3.connect('courses.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE id = ?', (id,))
        course = cursor.fetchone()
        conn.close()
        
        if course:
            return Course(
                id=course['id'],
                title=course['title'],
                description=course['description'],
                content=course['content'],
                created_at=course['created_at'],
                updated_at=course['updated_at']
            )
        return None

class CreateCourse(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        content = String(required=True)

    course = Field(Course)

    def mutate(self, info, title, description, content):
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO courses (title, description, content) VALUES (?, ?, ?)',
            (title, description, content)
        )
        course_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        course = cursor.fetchone()
        conn.close()

        return CreateCourse(course=Course(
            id=course[0],
            title=course[1],
            description=course[2],
            content=course[3],
            created_at=course[4],
            updated_at=course[5]
        ))

class Mutation(ObjectType):
    create_course = CreateCourse.Field()
