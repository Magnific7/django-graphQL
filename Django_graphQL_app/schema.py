import graphene

from .fields import(
    Graph_modalClass
)
from .models import (
    Graph_modal
)
from .mutations import(
    createGraphQl_modal,
    delete
)



class Query(graphene.ObjectType):
    graphqls = graphene.List(Graph_modalClass)
    grapgql_modal = graphene.Field(Graph_modalClass, user_id = graphene.ID())

    def resolve_graphqls(root,info):
        return Graph_modal.objects.all()
    
    def resolve_graphql(root,info, user_id):
        return Graph_modal.objects.get(user_id = user_id)


class Mutation(graphene.ObjectType):
    create_grapgql_modal = createGraphQl_modal.Field()
    delete = delete.Field()



schema = graphene.Schema(query = Query, mutation=Mutation)