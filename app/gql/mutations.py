import strawberry

from app.gql.post.mutation import PostMutation
from app.gql.user.mutation import UserMutation

@strawberry.type
class Mutation(PostMutation, UserMutation):
    pass


    


# By adding these mutation fields to the Mutation class, you're effectively exposing them 
#     in your GraphQL schema, making them accessible to clients through GraphQL queries.