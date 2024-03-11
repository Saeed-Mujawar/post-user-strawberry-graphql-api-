import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.db. models import Base
from app.db.database import engine
from app. gql.queries import Query
from app.gql.mutations import Mutation

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)

@app.get('/')
def home():
    return "welcome home!!"
   
schema = strawberry.Schema(query=Query, mutation= Mutation)

grapgql_app = GraphQLRouter(schema)

app.include_router(grapgql_app, prefix = "/graphql")
