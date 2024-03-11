import strawberry
from app.gql.post.query import PostQuery
from app.gql.user.query import UserQuery 

@strawberry.type
class Query(PostQuery, UserQuery):
    pass


 
