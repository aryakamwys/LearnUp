from graphene import ObjectType, String, Int, ID, Field, List, Mutation, InputObjectType, Boolean
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'courses.db')

# Type
class CourseType(ObjectType):
    id = ID()
    title = String()
    description = String()
    content = String()
    created_at = String()
    updated_at = String()

# Input Types
class CreateCourseInput(InputObjectType):
    title = String(required=True)
    description = String()
    content = String()

class UpdateCourseInput(InputObjectType):
    id = ID(required=True)
    title = String()
    description = String()
    content = String()

# Query
class Query(ObjectType):
    all_courses = List(CourseType)
    course = Field(CourseType, id=ID(required=True))

    def resolve_all_courses(root, info):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # ✅ penting agar bisa dict(row)
        rows = conn.execute("SELECT * FROM courses").fetchall()
        conn.close()
        return [CourseType(**dict(row)) for row in rows]

    def resolve_course(root, info, id):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # ✅
        row = conn.execute("SELECT * FROM courses WHERE id = ?", (id,)).fetchone()
        conn.close()
        return CourseType(**dict(row)) if row else None

# Mutations
class CreateCourse(Mutation):
    class Arguments:
        input = CreateCourseInput(required=True)

    Output = CourseType

    def mutate(root, info, input):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # ✅ fix error dict(row)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO courses (title, description, content)
            VALUES (?, ?, ?)
        """, (input.title, input.description, input.content))
        conn.commit()
        course_id = cursor.lastrowid
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        return CourseType(**dict(row))

class UpdateCourse(Mutation):
    class Arguments:
        input = UpdateCourseInput(required=True)

    Output = CourseType

    def mutate(root, info, input):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # ✅ fix konsisten
        conn.execute("""
            UPDATE courses
            SET title = ?, description = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (input.title, input.description, input.content, input.id))
        conn.commit()
        row = conn.execute("SELECT * FROM courses WHERE id = ?", (input.id,)).fetchone()
        conn.close()
        return CourseType(**dict(row)) if row else None

class DeleteCourse(Mutation):
    class Arguments:
        id = ID(required=True)

    Output = Boolean

    def mutate(root, info, id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ?", (id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

# Register mutations
class Mutation(ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
