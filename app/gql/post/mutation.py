import strawberry
from app.gql.schemas import PostObject
from app.db.database import Session
from app.db.models import Post
from app.utils import authorize_user_by_id, get_authenticated_user
from strawberry.types import Info


@strawberry.type
class PostMutation:

    @strawberry.mutation
    @staticmethod
    @authorize_user_by_id
    def add_post(root, info: Info, title: str, body: str, user_id: int) -> PostObject:
        post = Post(title=title, body=body, user_id=user_id)
        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)
        session.close()
        return post

    @strawberry.mutation
    @staticmethod
    @authorize_user_by_id
    def update_post(root, info: Info, post_id: int, user_id: int, title: str = None, body: str = None) -> PostObject:
        authenticated_user = get_authenticated_user(info.context)
        session = Session()
        post = session.query(Post).filter(Post.id == post_id, Post.user_id == authenticated_user.id).first()
        if not post:
            session.close()
            raise Exception("Post not found")
        if title is not None:
            post.title = title
        if body is not None:
            post.body = body
        session.commit()
        session.refresh(post)
        session.close()
        return post

    @strawberry.mutation
    @staticmethod
    @authorize_user_by_id
    def delete_post(root, info: Info, post_id: int, user_id: int) -> bool:
        authenticated_user = get_authenticated_user(info.context)
        session = Session()
        post = session.query(Post).filter(Post.id == post_id, Post.user_id == authenticated_user.id).first()
        if not post:
            session.close()
            raise Exception("Post not found")
        session.delete(post)
        session.commit()
        session.close()
        return True