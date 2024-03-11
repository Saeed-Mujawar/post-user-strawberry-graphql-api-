import strawberry
from typing import List
from app.gql.schemas import PostObject
from app.db.database import Session
from app.db.models import Post

@strawberry.type
class PostQuery:
    posts: List['PostObject']
    post: 'PostObject'
    
    @strawberry.field
    def resolve_posts(root, info) -> List['PostObject']:
        return Session().query(Post).all()

    @strawberry.field
    def resolve_post(root, info, post_id: int) -> 'PostObject':
        return Session().query(Post).filter(Post.id == post_id).first()
