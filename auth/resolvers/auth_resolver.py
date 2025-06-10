import jwt
import bcrypt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from database import db_session
from auth.models.user import User
from auth.models.session import Session

SECRET_KEY = "your-secret-key"  # In production, use environment variable

class AuthResolver:
    @staticmethod
    def register(username, email, password):
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash.decode('utf-8')
            )
            
            db_session.add(user)
            db_session.commit()
            
            # Generate token
            token = AuthResolver.create_token(user)
            
            return {
                'success': True,
                'message': 'Registration successful',
                'token': token,
                'user': user.to_dict()
            }
            
        except IntegrityError:
            db_session.rollback()
            return {
                'success': False,
                'message': 'Username or email already exists',
                'token': None,
                'user': None
            }
        except Exception as e:
            db_session.rollback()
            return {
                'success': False,
                'message': str(e),
                'token': None,
                'user': None
            }

    @staticmethod
    def login(email, password):
        try:
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return {
                    'success': False,
                    'message': 'Invalid email or password',
                    'token': None,
                    'user': None
                }
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return {
                    'success': False,
                    'message': 'Invalid email or password',
                    'token': None,
                    'user': None
                }
            
            token = AuthResolver.create_token(user)
            
            return {
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'token': None,
                'user': None
            }

    @staticmethod
    def create_token(user):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # Create session
        session = Session(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        
        db_session.add(session)
        db_session.commit()
        
        return token

    @staticmethod
    def get_current_user(info):
        auth_header = info.context.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            session = Session.query.filter_by(
                user_id=user_id,
                token=token,
                expires_at={'$gt': datetime.utcnow()}
            ).first()
            
            if not session:
                return None
                
            return User.query.get(user_id)
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None 