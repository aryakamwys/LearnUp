# app/schema.py

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Loan, SessionLocal
import datetime

class LoanType(SQLAlchemyObjectType):
    class Meta:
        model = Loan

class Query(graphene.ObjectType):
    all_loans = graphene.List(LoanType)
    loan_by_id = graphene.Field(LoanType, id=graphene.Int(required=True))
    loans_by_user = graphene.List(LoanType, user_id=graphene.Int(required=True))
    loans_by_course = graphene.List(LoanType, course_id=graphene.Int(required=True))

    def resolve_all_loans(self, info):
        session = SessionLocal()
        try:
            return session.query(Loan).all()
        finally:
            session.close()

    def resolve_loan_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(Loan).filter(Loan.id == id).first()
        finally:
            session.close()

    def resolve_loans_by_user(self, info, user_id):
        session = SessionLocal()
        try:
            return session.query(Loan).filter(Loan.user_id == user_id).all()
        finally:
            session.close()

    def resolve_loans_by_course(self, info, course_id):
        session = SessionLocal()
        try:
            return session.query(Loan).filter(Loan.course_id == course_id).all()
        finally:
            session.close()

class CreateLoan(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        course_id = graphene.Int(required=True)

    loan = graphene.Field(LoanType)
    ok = graphene.Boolean()

    def mutate(self, info, user_id, course_id):
        session = SessionLocal()
        try:
            loan = Loan(user_id=user_id, course_id=course_id)
            session.add(loan)
            session.commit()
            session.refresh(loan)
            return CreateLoan(loan=loan, ok=True)
        except Exception as e:
            session.rollback()
            return CreateLoan(loan=None, ok=False)
        finally:
            session.close()

class ReturnLoan(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    loan = graphene.Field(LoanType)
    ok = graphene.Boolean()

    def mutate(self, info, id):
        session = SessionLocal()
        try:
            loan = session.query(Loan).filter(Loan.id == id).first()
            if loan:
                loan.is_returned = True
                loan.return_date = datetime.datetime.now()
                session.commit()
                session.refresh(loan)
                return ReturnLoan(loan=loan, ok=True)
            return ReturnLoan(loan=None, ok=False)
        except Exception as e:
            session.rollback()
            return ReturnLoan(loan=None, ok=False)
        finally:
            session.close()

class DeleteLoan(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        session = SessionLocal()
        try:
            loan = session.query(Loan).filter(Loan.id == id).first()
            if loan:
                session.delete(loan)
                session.commit()
                return DeleteLoan(ok=True)
            return DeleteLoan(ok=False)
        except Exception as e:
            session.rollback()
            return DeleteLoan(ok=False)
        finally:
            session.close()

class DeleteAllLoans(graphene.Mutation):
    ok = graphene.Boolean()
    count = graphene.Int()

    def mutate(root, info):
        session = SessionLocal()
        try:
            count = session.query(Loan).delete()
            session.commit()
            return DeleteAllLoans(ok=True, count=count)
        except Exception as e:
            session.rollback()
            return DeleteAllLoans(ok=False, count=0)
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_loan = CreateLoan.Field()
    return_loan = ReturnLoan.Field()
    delete_loan = DeleteLoan.Field()
    delete_all_loans = DeleteAllLoans.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)