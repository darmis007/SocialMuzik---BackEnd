from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id = graphene.Int())
    me = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()
    
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self,info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged In')
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
    
    def mutate(self, info, **kwargs):
        user = get_user_model()(
            username = kwargs.get('username'),
            email = kwargs.get('email'),
        )
        user.set_password(kwargs.get('password'))
        user.save()
        return CreateUser(user = user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
