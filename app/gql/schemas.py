from typing import List
import strawberry

@strawberry.type
class UserObject:
    id : int
    username : str
    email: str
    posts: List['PostObject']

    
@strawberry.type
class PostObject:
    id: int
    title: str
    body: str
    user_id: int
    user: 'UserObject' 


@strawberry.type
class AuthPayload:
    token: str
    
    