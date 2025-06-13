import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from database import db_session
from models.quiz import Quiz
from models.question import Question
from models.option import Option
from models.quiz_result import QuizResult

# GraphQL Types
class QuizType(SQLAlchemyObjectType):
    class Meta:
        model = Quiz

class QuestionType(SQLAlchemyObjectType):
    class Meta:
        model = Question

class OptionType(SQLAlchemyObjectType):
    class Meta:
        model = Option

class QuizResultType(SQLAlchemyObjectType):
    class Meta:
        model = QuizResult

# Queries
class Query(graphene.ObjectType):
    quizzes = graphene.List(QuizType)
    quiz = graphene.Field(QuizType, id=graphene.Int(required=True))
    questions = graphene.List(QuestionType, quiz_id=graphene.Int())
    options = graphene.List(OptionType, question_id=graphene.Int())

    def resolve_quizzes(self, info):
        return db_session.query(Quiz).filter_by(is_active=1).all()

    def resolve_quiz(self, info, id):
        return db_session.query(Quiz).filter_by(id=id, is_active=1).first()

    def resolve_questions(self, info, quiz_id=None):
        query = db_session.query(Question)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
        return query.order_by(Question.order_index).all()

    def resolve_options(self, info, question_id=None):
        query = db_session.query(Option)
        if question_id:
            query = query.filter_by(question_id=question_id)
        return query.all()

# Mutations
class CreateQuiz(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        time_limit = graphene.Int()
        passing_score = graphene.Int()

    quiz = graphene.Field(lambda: QuizType)

    def mutate(self, info, title, description=None, time_limit=0, passing_score=70):
        quiz = Quiz(
            title=title,
            description=description,
            time_limit=time_limit,
            passing_score=passing_score
        )
        db_session.add(quiz)
        db_session.commit()
        return CreateQuiz(quiz=quiz)

class CreateQuestion(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        question_text = graphene.String(required=True)
        question_type = graphene.String()
        points = graphene.Int()

    question = graphene.Field(lambda: QuestionType)

    def mutate(self, info, quiz_id, question_text, question_type='multiple_choice', points=1):
        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=question_type,
            points=points
        )
        db_session.add(question)
        db_session.commit()
        return CreateQuestion(question=question)

class CreateOption(graphene.Mutation):
    class Arguments:
        question_id = graphene.Int(required=True)
        option_text = graphene.String(required=True)
        is_correct = graphene.Boolean()

    option = graphene.Field(lambda: OptionType)

    def mutate(self, info, question_id, option_text, is_correct=False):
        option = Option(
            question_id=question_id,
            option_text=option_text,
            is_correct=is_correct
        )
        db_session.add(option)
        db_session.commit()
        return CreateOption(option=option)

class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    create_question = CreateQuestion.Field()
    create_option = CreateOption.Field() 