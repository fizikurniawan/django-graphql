from graphene_django import DjangoObjectType
import graphene
from .models import Profile

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class ProfileMuatation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        email = graphene.String(required=True)

    # The class attributes define the response of the mutation
    profile = graphene.Field(ProfileType)

    def mutate(self, info, firstName, lastName, email):
        profile = Profile.objects.create(first_name=firstName, last_name=lastName, email = email)
        # Notice we return an instance of this mutation
        return ProfileMuatation(profile=profile)

class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType)
    profile = graphene.Field(ProfileType, id=graphene.Int())

    def resolve_profiles(self, info):
        return Profile.objects.all()
    
    def resolve_profile(self, info, **kwargs):
        return Profile.objects.get(id = kwargs.get('id'))

class Mutation(graphene.ObjectType):
    profile_mutation = ProfileMuatation.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)
