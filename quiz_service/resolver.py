import graphene
from datetime import datetime

from models.quiz import Quiz
from models.question import Question
from models.option import Option
from models.quiz_result import QuizResult
from database import db_session


# === GRAPHQL TYPES ===

class OptionType(graphene.ObjectType):
    id = graphene.ID()
    question_id = graphene.Int()
    option_text = graphene.String()
    is_correct = graphene.Boolean()
    order_index = graphene.Int()


class QuestionType(graphene.ObjectType):
    id = graphene.ID()
    quiz_id = graphene.Int()
    question_text = graphene.String()
    question_type = graphene.String()
    points = graphene.Int()
    order_index = graphene.Int()
    options = graphene.List(OptionType)

    def resolve_options(self, info):
        return db_session.query(Option).filter_by(question_id=self.id).order_by(Option.order_index).all()


class QuizType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    course_id = graphene.Int()
    created_by = graphene.Int()
    time_limit = graphene.Int()
    passing_score = graphene.Int()
    is_active = graphene.Int()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    questions = graphene.List(QuestionType)

    def resolve_questions(self, info):
        return db_session.query(Question).filter_by(quiz_id=self.id).order_by(Question.order_index).all()


class QuizResultType(graphene.ObjectType):
    id = graphene.ID()
    quiz_id = graphene.Int()
    user_id = graphene.Int()
    score = graphene.Float()
    total_questions = graphene.Int()
    correct_answers = graphene.Int()
    time_taken = graphene.Int()
    passed = graphene.Int()
    started_at = graphene.DateTime()
    completed_at = graphene.DateTime()


# === MUTATIONS ===

class CreateQuiz(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        course_id = graphene.Int()
        created_by = graphene.Int()
        time_limit = graphene.Int()
        passing_score = graphene.Int()

    ok = graphene.Boolean()
    quiz = graphene.Field(lambda: QuizType)
    message = graphene.String()

    def mutate(self, info, title, description=None, course_id=None, created_by=None, time_limit=0, passing_score=70):
        quiz = Quiz(
            title=title,
            description=description,
            course_id=course_id,
            created_by=created_by,
            time_limit=time_limit,
            passing_score=passing_score
        )
        db_session.add(quiz)
        db_session.commit()

        return CreateQuiz(ok=True, quiz=quiz, message="Quiz created successfully.")


class CreateQuestion(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        question_text = graphene.String(required=True)
        question_type = graphene.String()
        points = graphene.Int()
        order_index = graphene.Int()

    ok = graphene.Boolean()
    question = graphene.Field(lambda: QuestionType)
    message = graphene.String()

    def mutate(self, info, quiz_id, question_text, question_type='multiple_choice', points=1, order_index=0):
        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=question_type,
            points=points,
            order_index=order_index
        )
        db_session.add(question)
        db_session.commit()

        return CreateQuestion(ok=True, question=question, message="Question created successfully.")


class CreateOption(graphene.Mutation):
    class Arguments:
        question_id = graphene.Int(required=True)
        option_text = graphene.String(required=True)
        is_correct = graphene.Boolean()
        order_index = graphene.Int()

    ok = graphene.Boolean()
    option = graphene.Field(lambda: OptionType)
    message = graphene.String()

    def mutate(self, info, question_id, option_text, is_correct=False, order_index=0):
        option = Option(
            question_id=question_id,
            option_text=option_text,
            is_correct=is_correct,
            order_index=order_index
        )
        db_session.add(option)
        db_session.commit()

        return CreateOption(ok=True, option=option, message="Option created successfully.")


class SubmitQuizResult(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        user_id = graphene.Int()
        score = graphene.Float(required=True)
        total_questions = graphene.Int(required=True)
        correct_answers = graphene.Int(required=True)
        time_taken = graphene.Int()
        answers = graphene.List(graphene.Int)  # List of selected option IDs

    ok = graphene.Boolean()
    result = graphene.Field(lambda: QuizResultType)
    message = graphene.String()

    def mutate(self, info, quiz_id, score, total_questions, correct_answers, user_id=None, time_taken=None, answers=None):
        # Get quiz to check passing score
        quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()
        if not quiz:
            return SubmitQuizResult(ok=False, result=None, message="Quiz not found.")

        passed = 1 if score >= quiz.passing_score else 0

        result = QuizResult(
            quiz_id=quiz_id,
            user_id=user_id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            time_taken=time_taken,
            passed=passed
        )
        db_session.add(result)
        db_session.commit()

        return SubmitQuizResult(ok=True, result=result, message="Quiz result submitted successfully.")


# === QUERIES ===

class Query(graphene.ObjectType):
    quizzes = graphene.List(QuizType, course_id=graphene.Int())
    quiz = graphene.Field(QuizType, id=graphene.Int(required=True))
    questions = graphene.List(QuestionType, quiz_id=graphene.Int(required=True))
    quiz_results = graphene.List(QuizResultType, quiz_id=graphene.Int(), user_id=graphene.Int())

    def resolve_quizzes(self, info, course_id=None):
        query = db_session.query(Quiz).filter_by(is_active=1)
        if course_id:
            query = query.filter_by(course_id=course_id)
        return query.all()

    def resolve_quiz(self, info, id):
        return db_session.query(Quiz).filter_by(id=id).first()

    def resolve_questions(self, info, quiz_id):
        return db_session.query(Question).filter_by(quiz_id=quiz_id).order_by(Question.order_index).all()

    def resolve_quiz_results(self, info, quiz_id=None, user_id=None):
        query = db_session.query(QuizResult)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.order_by(QuizResult.completed_at.desc()).all()


# === MUTATION ENTRYPOINT ===

class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    create_question = CreateQuestion.Field()
    create_option = CreateOption.Field()
    submit_quiz_result = SubmitQuizResult.Field() 