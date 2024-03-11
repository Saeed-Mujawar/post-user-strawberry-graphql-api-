from app.gql.schemas import UserObject, AuthPayload
from app.db.database import Session
from app.db.models import User, Post
from app.utils import generate_token, verify_password, hash_password, authorize_user_by_id
import strawberry
from strawberry.types import Info


@strawberry.type
class UserMutation:

    @strawberry.mutation
    @staticmethod
    def login_user(root, info: Info, email: str, password: str) -> AuthPayload:
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("A user with that email does not exist")
        
        verify_password(user.password_hash, password)
            
        
        token = generate_token(user.id)
        return AuthPayload(token=token)

    @strawberry.mutation
    @staticmethod
    def add_user(root, info: Info, username: str, email: str, password: str) -> UserObject:
        session = Session()
        existing_user = session.query(User).filter(User.email == email).first()

        if existing_user:
            raise ValueError("A user with that email already exists")

        password_hash = hash_password(password)
        user = User(username=username, email=email, password_hash=password_hash)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @strawberry.mutation
    @staticmethod
    @authorize_user_by_id
    def delete_user(root, info : Info , user_id: int) -> bool:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError("User not found")
        
        user_posts = session.query(Post).filter(Post.user_id == user_id).all()
        for post in user_posts:
            session.delete(post)
        
        session.delete(user)
        session.commit()
        session.close()
        return True
    
    @strawberry.mutation
    @staticmethod
    @authorize_user_by_id
    def update_user(root, info: Info, user_id: int, username: str = None, email: str = None, password: str = None) -> UserObject:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError("User not found")

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            if not password:
                raise ValueError("Password cannot be empty")
            password_hash = hash_password(password)
            user.password_hash = password_hash

        session.commit()
        session.refresh(user)
        session.close()
        return user
    
