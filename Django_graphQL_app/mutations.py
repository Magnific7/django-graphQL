import graphene
from .fields import Graph_modalClass
from .models import Graph_modal

class createGraphQl_modal(graphene.Mutation):
    error = graphene.String()
    success = graphene.Boolean()
    grapgql_modal = graphene.Field(Graph_modalClass)
    
    class Meta:
        description = "Add user details"

    class Arguments:
        user_id = graphene.String()
        user_name = graphene.String()
        user_first_name = graphene.String()
        user_last_name = graphene.String()
        user_email = graphene.String()
        user_status = graphene.String()
        user_phone_number = graphene.String()

    def mutate(self, info, **kwargs):
        try:
            grapgql_modal = Graph_modal.objects.create(
                user_id=kwargs.get('user_id'),
                    user_name=kwargs.get('user_name'), user_first_name=kwargs.get('user_first_name'),
                    user_last_name=kwargs.get('user_last_name'),user_email=kwargs.get('user_email'),user_status=kwargs.get('user_status'),user_phone_number=kwargs.get('user_phone_number')
            )
            
            return createGraphQl_modal(success = True, grapgql_modal = grapgql_modal)
        except Exception as e:
            return createGraphQl_modal(success = False, error = e)

class delete(graphene.Mutation):
    error = graphene.String()
    success = graphene.Boolean()
    
    class Arguments:
        user_id = graphene.ID()

    def mutate(self, info, **kwargs):
        try:
            if(kwargs.get('user_id')):
                Graph_modal.objects.filter(user_id = kwargs.get('user_id')).delete()
            return delete(success = True)
        except Exception as e:
            return delete(success= False, error = e)
            