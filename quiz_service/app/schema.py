# app/schema.py

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Quiz, QuizQuestion, QuizAttempt, SessionLocal
import datetime

class QuizType(SQLAlchemyObjectType):
    class Meta:
        model = Quiz

class QuizQuestionType(SQLAlchemyObjectType):
    class Meta:
        model = QuizQuestion

class QuizAttemptType(SQLAlchemyObjectType):
    class Meta:
        model = QuizAttempt

class Query(graphene.ObjectType):
    all_quizzes = graphene.List(QuizType)
    quiz_by_id = graphene.Field(QuizType, id=graphene.Int(required=True))
    quizzes_by_course = graphene.List(QuizType, course_id=graphene.Int(required=True))
    active_quizzes = graphene.List(QuizType)
    
    all_questions = graphene.List(QuizQuestionType)
    questions_by_quiz = graphene.List(QuizQuestionType, quiz_id=graphene.Int(required=True))
    question_by_id = graphene.Field(QuizQuestionType, id=graphene.Int(required=True))
    
    all_attempts = graphene.List(QuizAttemptType)
    attempts_by_user = graphene.List(QuizAttemptType, user_id=graphene.Int(required=True))
    attempts_by_quiz = graphene.List(QuizAttemptType, quiz_id=graphene.Int(required=True))
    attempt_by_id = graphene.Field(QuizAttemptType, id=graphene.Int(required=True))

    def resolve_all_quizzes(self, info):
        session = SessionLocal()
        try:
            return session.query(Quiz).all()
        finally:
            session.close()

    def resolve_quiz_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(Quiz).filter(Quiz.id == id).first()
        finally:
            session.close()

    def resolve_quizzes_by_course(self, info, course_id):
        session = SessionLocal()
        try:
            return session.query(Quiz).filter(Quiz.course_id == course_id).all()
        finally:
            session.close()

    def resolve_active_quizzes(self, info):
        session = SessionLocal()
        try:
            return session.query(Quiz).filter(Quiz.is_active == True).all()
        finally:
            session.close()

    def resolve_all_questions(self, info):
        session = SessionLocal()
        try:
            return session.query(QuizQuestion).all()
        finally:
            session.close()

    def resolve_questions_by_quiz(self, info, quiz_id):
        session = SessionLocal()
        try:
            return session.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
        finally:
            session.close()

    def resolve_question_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(QuizQuestion).filter(QuizQuestion.id == id).first()
        finally:
            session.close()

    def resolve_all_attempts(self, info):
        session = SessionLocal()
        try:
            return session.query(QuizAttempt).all()
        finally:
            session.close()

    def resolve_attempts_by_user(self, info, user_id):
        session = SessionLocal()
        try:
            return session.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
        finally:
            session.close()

    def resolve_attempts_by_quiz(self, info, quiz_id):
        session = SessionLocal()
        try:
            return session.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id).all()
        finally:
            session.close()

    def resolve_attempt_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(QuizAttempt).filter(QuizAttempt.id == id).first()
        finally:
            session.close()

class CreateQuiz(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        course_id = graphene.Int(required=True)

    quiz = graphene.Field(QuizType)
    ok = graphene.Boolean()

    def mutate(self, info, title, course_id, description=None):
        session = SessionLocal()
        try:
            quiz = Quiz(title=title, description=description, course_id=course_id)
            session.add(quiz)
            session.commit()
            session.refresh(quiz)
            return CreateQuiz(quiz=quiz, ok=True)
        except Exception as e:
            session.rollback()
            return CreateQuiz(quiz=None, ok=False)
        finally:
            session.close()

class CreateQuizQuestion(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        question_text = graphene.String(required=True)
        option_a = graphene.String(required=True)
        option_b = graphene.String(required=True)
        option_c = graphene.String(required=True)
        option_d = graphene.String(required=True)
        correct_answer = graphene.String(required=True)
        points = graphene.Int()

    question = graphene.Field(QuizQuestionType)
    ok = graphene.Boolean()

    def mutate(self, info, quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer, points=1):
        session = SessionLocal()
        try:
            question = QuizQuestion(
                quiz_id=quiz_id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer.upper(),
                points=points
            )
            session.add(question)
            session.commit()
            session.refresh(question)
            return CreateQuizQuestion(question=question, ok=True)
        except Exception as e:
            session.rollback()
            return CreateQuizQuestion(question=None, ok=False)
        finally:
            session.close()

class StartQuizAttempt(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        quiz_id = graphene.Int(required=True)

    attempt = graphene.Field(QuizAttemptType)
    ok = graphene.Boolean()

    def mutate(self, info, user_id, quiz_id):
        session = SessionLocal()
        try:
            # Check if quiz exists and is active
            quiz = session.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
            if not quiz:
                return StartQuizAttempt(attempt=None, ok=False)
            
            # Calculate total points for the quiz
            total_points = session.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).count()
            
            attempt = QuizAttempt(user_id=user_id, quiz_id=quiz_id, total_points=total_points)
            session.add(attempt)
            session.commit()
            session.refresh(attempt)
            return StartQuizAttempt(attempt=attempt, ok=True)
        except Exception as e:
            session.rollback()
            return StartQuizAttempt(attempt=None, ok=False)
        finally:
            session.close()

class CompleteQuizAttempt(graphene.Mutation):
    class Arguments:
        attempt_id = graphene.Int(required=True)
        score = graphene.Int(required=True)

    attempt = graphene.Field(QuizAttemptType)
    ok = graphene.Boolean()

    def mutate(self, info, attempt_id, score):
        session = SessionLocal()
        try:
            attempt = session.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
            if attempt:
                attempt.score = score
                attempt.completed_at = datetime.datetime.now()
                attempt.is_completed = True
                session.commit()
                session.refresh(attempt)
                return CompleteQuizAttempt(attempt=attempt, ok=True)
            return CompleteQuizAttempt(attempt=None, ok=False)
        except Exception as e:
            session.rollback()
            return CompleteQuizAttempt(attempt=None, ok=False)
        finally:
            session.close()

class UpdateQuiz(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        is_active = graphene.Boolean()

    quiz = graphene.Field(QuizType)
    ok = graphene.Boolean()

    def mutate(self, info, id, title=None, description=None, is_active=None):
        session = SessionLocal()
        try:
            quiz = session.query(Quiz).filter(Quiz.id == id).first()
            if quiz:
                if title is not None:
                    quiz.title = title
                if description is not None:
                    quiz.description = description
                if is_active is not None:
                    quiz.is_active = is_active
                session.commit()
                session.refresh(quiz)
                return UpdateQuiz(quiz=quiz, ok=True)
            return UpdateQuiz(quiz=None, ok=False)
        except Exception as e:
            session.rollback()
            return UpdateQuiz(quiz=None, ok=False)
        finally:
            session.close()

class DeleteQuiz(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        session = SessionLocal()
        try:
            quiz = session.query(Quiz).filter(Quiz.id == id).first()
            if quiz:
                session.delete(quiz)
                session.commit()
                return DeleteQuiz(ok=True)
            return DeleteQuiz(ok=False)
        except Exception as e:
            session.rollback()
            return DeleteQuiz(ok=False)
        finally:
            session.close()

class DeleteQuizQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        session = SessionLocal()
        try:
            question = session.query(QuizQuestion).filter(QuizQuestion.id == id).first()
            if question:
                session.delete(question)
                session.commit()
                return DeleteQuizQuestion(ok=True)
            return DeleteQuizQuestion(ok=False)
        except Exception as e:
            session.rollback()
            return DeleteQuizQuestion(ok=False)
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    create_quiz_question = CreateQuizQuestion.Field()
    start_quiz_attempt = StartQuizAttempt.Field()
    complete_quiz_attempt = CompleteQuizAttempt.Field()
    update_quiz = UpdateQuiz.Field()
    delete_quiz = DeleteQuiz.Field()
    delete_quiz_question = DeleteQuizQuestion.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 