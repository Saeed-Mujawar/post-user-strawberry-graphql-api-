import strawberry
from typing import List
from app.gql.schemas import UserObject
from app.db.database import Session
from app.db.models import User

@strawberry.type
class UserQuery:
    users: List[UserObject]
    user: UserObject

    @strawberry.field
    async def resolve_users(root, info) -> List[UserObject]:
        return await Session().query(User).all()

    @strawberry.field
    async def resolve_user(root, info, user_id: int) -> UserObject:
        return await Session().query(User).filter(User.id == user_id).first()