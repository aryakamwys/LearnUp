import graphene
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from database import db_session


# === GRAPHQL TYPE ===
class UserType(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()


# === MUTATIONS ===

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)
    message = graphene.String()

    def mutate(self, info, username, email, password):
        # Prevent duplicate username/email
        existing = db_session.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing:
            return RegisterUser(ok=False, message="User already exists.", user=None)

        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db_session.add(user)
        db_session.commit()

        return RegisterUser(ok=True, user=user, message="User registered successfully.")


class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)
    message = graphene.String()

    def mutate(self, info, username, password):
        user = db_session.query(User).filter_by(username=username).first()

        if not user:
            return LoginUser(ok=False, user=None, message="User not found.")

        if not check_password_hash(user.password_hash, password):
            return LoginUser(ok=False, user=None, message="Incorrect password.")

        return LoginUser(ok=True, user=user, message="Login successful.")


# === QUERY ===

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return db_session.query(User).all()


# === MUTATION ENTRYPOINT ===

class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
