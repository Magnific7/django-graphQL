import graphene
from graphene_django import DjangoObjectType
from .models import Graph_modal

class Graph_modalClass(DjangoObjectType):
    class Meta:
       model = Graph_modal
