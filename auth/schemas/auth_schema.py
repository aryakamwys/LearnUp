import graphene
from graphene import String, Field, ObjectType, Mutation
from auth.resolvers.auth_resolver import AuthResolver

class User(ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    created_at = graphene.String()

class AuthResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    token = graphene.String()
    user = graphene.Field(User)

class Register(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    Output = AuthResponse

    def mutate(self, info, username, email, password):
        return AuthResolver.register(username, email, password)

class Login(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    Output = AuthResponse

    def mutate(self, info, email, password):
        return AuthResolver.login(email, password)

class AuthMutation(ObjectType):
    register = Register.Field()
    login = Login.Field()

class AuthQuery(ObjectType):
    me = Field(User)
    
    def resolve_me(self, info):
        return AuthResolver.get_current_user(info) 