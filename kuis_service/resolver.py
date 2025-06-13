import graphene
from database import db_session
from models.quiz import Quiz
from models.question import Question
from models.option import Option
from models.quiz_result import QuizResult

# GraphQL Types (Manual Definition)
class QuizType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    time_limit = graphene.Int()
    passing_score = graphene.Int()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    questions = graphene.List(lambda: QuestionType)
    quiz_results = graphene.List(lambda: QuizResultType)

    def resolve_questions(self, info):
        return db_session.query(Question).filter_by(quiz_id=self.id, is_active=True).all()

    def resolve_quiz_results(self, info):
        return db_session.query(QuizResult).filter_by(quiz_id=self.id).all()


class QuestionType(graphene.ObjectType):
    id = graphene.Int()
    quiz_id = graphene.Int()
    question_text = graphene.String()
    question_type = graphene.String()
    points = graphene.Int()
    order_index = graphene.Int()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    quiz = graphene.Field(lambda: QuizType)
    options = graphene.List(lambda: OptionType)

    def resolve_quiz(self, info):
        return db_session.query(Quiz).filter_by(id=self.quiz_id).first()

    def resolve_options(self, info):
        return db_session.query(Option).filter_by(question_id=self.id).all()


class OptionType(graphene.ObjectType):
    id = graphene.Int()
    question_id = graphene.Int()
    option_text = graphene.String()
    is_correct = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    question = graphene.Field(lambda: QuestionType)

    def resolve_question(self, info):
        return db_session.query(Question).filter_by(id=self.question_id).first()


class QuizResultType(graphene.ObjectType):
    id = graphene.Int()
    quiz_id = graphene.Int()
    user_id = graphene.Int()
    score = graphene.Int()
    time_taken = graphene.Int()
    completed_at = graphene.DateTime()

    quiz = graphene.Field(lambda: QuizType)

    def resolve_quiz(self, info):
        return db_session.query(Quiz).filter_by(id=self.quiz_id).first()


# Queries
class Query(graphene.ObjectType):
    quizzes = graphene.List(QuizType)
    quiz = graphene.Field(QuizType, id=graphene.Int(required=True))
    questions = graphene.List(QuestionType, quiz_id=graphene.Int())
    options = graphene.List(OptionType, question_id=graphene.Int())
    quiz_results = graphene.List(QuizResultType, user_id=graphene.Int(), quiz_id=graphene.Int())

    def resolve_quizzes(self, info):
        # Implement role-based access here if needed (e.g., only admin sees inactive quizzes)
        return db_session.query(Quiz).filter_by(is_active=True).all()

    def resolve_quiz(self, info, id):
        return db_session.query(Quiz).filter_by(id=id, is_active=True).first()

    def resolve_questions(self, info, quiz_id=None):
        query = db_session.query(Question)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
        return query.filter_by(is_active=True).order_by(Question.order_index).all()

    def resolve_options(self, info, question_id=None):
        query = db_session.query(Option)
        if question_id:
            query = query.filter_by(question_id=question_id)
        return query.all()

    def resolve_quiz_results(self, info, user_id=None, quiz_id=None):
        query = db_session.query(QuizResult)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if quiz_id:
            query = query.filter_by(quiz_id=quiz_id)
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

class UpdateQuiz(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        time_limit = graphene.Int()
        passing_score = graphene.Int()
        is_active = graphene.Boolean()

    quiz = graphene.Field(lambda: QuizType)

    def mutate(self, info, id, title=None, description=None, time_limit=None, passing_score=None, is_active=None):
        quiz = db_session.query(Quiz).filter_by(id=id).first()
        if not quiz:
            raise Exception("Quiz not found!")

        if title is not None:
            quiz.title = title
        if description is not None:
            quiz.description = description
        if time_limit is not None:
            quiz.time_limit = time_limit
        if passing_score is not None:
            quiz.passing_score = passing_score
        if is_active is not None:
            quiz.is_active = is_active
        
        db_session.commit()
        return UpdateQuiz(quiz=quiz)

class DeleteQuiz(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        quiz = db_session.query(Quiz).filter_by(id=id).first()
        if not quiz:
            raise Exception("Quiz not found!")

        quiz.is_active = False # Soft delete
        db_session.commit()
        return DeleteQuiz(message="Quiz deleted successfully (soft delete)")

class CreateQuestion(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        question_text = graphene.String(required=True)
        question_type = graphene.String()
        points = graphene.Int()
        order_index = graphene.Int()

    question = graphene.Field(lambda: QuestionType)

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

class CreateQuizResult(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        score = graphene.Int()
        time_taken = graphene.Int()

    quiz_result = graphene.Field(lambda: QuizResultType)

    def mutate(self, info, quiz_id, user_id, score=0, time_taken=0):
        quiz_result = QuizResult(
            quiz_id=quiz_id,
            user_id=user_id,
            score=score,
            time_taken=time_taken
        )
        db_session.add(quiz_result)
        db_session.commit()
        return CreateQuizResult(quiz_result=quiz_result)


class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    update_quiz = UpdateQuiz.Field()
    delete_quiz = DeleteQuiz.Field()
    create_question = CreateQuestion.Field()
    create_option = CreateOption.Field()
    create_quiz_result = CreateQuizResult.Field() 