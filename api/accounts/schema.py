import graphene
from graphql_relay.node.node import from_global_id
from graphql import GraphQLError
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from .models import User
from .types import UserType


class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserType, search=graphene.String())

    user = graphene.relay.Node.Field(UserType)
    me = graphene.Field(UserType)

    def resolve_users(root, info, search=None, **kwargs):
        if search:
            filter = (
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
            return User.objects.filter(filter)
        return User.objects.all()


    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Not signed in')
        if not user.is_verified:
            raise GraphQLError('Not verified')
        return user

    def resolve_user(root, info, **kwargs):
        return User.objects.get(id=kwargs.get('id'))

        
class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(
            self, info, username, password):
        user = User(
            username=username,
            password=password
        )
        user.set_password(password)
        user.save()
        return UserCreate(user=user)


class UserDelete(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_admin == False):
            raise GraphQLError('Need to be at least an admin')
        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        user.is_deleted = True
        user.save()
        return UserDelete(user=user)


class UserDeleteFinal(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_admin == False):
            raise GraphQLError('Need to be at least an admin')
        user = User.objects.get(pk=from_global_id(input.get('id'))[1])

        user.delete()
        return UserDeleteFinal(user=user)


class NamesUpdate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, first_name, last_name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Sign in to update')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return NamesUpdate(user=user)


class EmailUpdate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Sign in to update')
        user.email = email
        user.save()
        return EmailUpdate(user=user)


class AvatarUpdate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        avatar = graphene.String()

    def mutate(self, info, avatar):
        user = info.context.user
        # image_data = info.context.FILES.get(image)
        if user.avatar:
            user.avatar.delete()
        user.avatar = avatar
        # user.avatar = image_data
        user.save()
        return AvatarUpdate(user=user)


class BirthDayUpdate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        birth_date = graphene.String(required=True)

    def mutate(self, info, birth_date):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Sign in to update')
        user.birth_date = birth_date
        user.save()
        return BirthDayUpdate(user=user)


class GenderUpdate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        gender = graphene.String(required=True)

    def mutate(self, info, gender):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Sign in to update')
        user.gender = gender
        user.save()
        return GenderUpdate(user=user)


class PasswordReset(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)

    def mutate(self, info, password):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Sign in to update')
        user.password = password
        user.save()
        return PasswordReset(user=user)


class StaffToggle(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()
        is_staff = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_admin == False):
            raise GraphQLError('Need to be at least an admin user')

        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        status = input.get('is_staff')
        user.is_staff = status
        user.save()
        return StaffToggle(user=user)


class AdminToggle(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()
        is_admin = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_superuser == False):
            raise GraphQLError('Need to be a superuser')

        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        status = input.get('is_admin')
        user.is_admin = status
        user.save()
        return AdminToggle(user=user)


class SupperToggle(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()
        is_superuser = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_superuser == False):
            raise GraphQLError('Need to be a superuser')

        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        status = input.get('is_superuser')
        user.is_superuser = status
        user.save()
        return SupperToggle(user=user)


class ActiveToggle(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()
        is_active = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        owner = info.context.user
        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        if (owner != user):
            raise GraphQLError('Need to be account owner')

        status = input.get('is_active')
        user.is_active = status
        user.save()
        return ActiveToggle(user=user)


class ActivedToggle(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        id = graphene.ID()
        is_active = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        adminuser = info.context.user
        if (adminuser.is_admin == False):
            raise GraphQLError('Need to be at least an admin')

        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        status = input.get('is_active')
        user.is_active = status
        user.save()
        return ActivedToggle(user=user)



class Mutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    password_reset = PasswordReset.Field()
    user_delete = UserDelete.Field()
    user_deletefinal = UserDeleteFinal.Field()
    names_update = NamesUpdate.Field()
    email_update = EmailUpdate.Field()
    avatar_update = AvatarUpdate.Field()
    birthday_update = BirthDayUpdate.Field()
    gender_update = GenderUpdate.Field()
    staff_toggle = StaffToggle.Field()
    admin_toggle = AdminToggle.Field()
    super_toggle = SupperToggle.Field()
    active_toggle = ActiveToggle.Field()
    activated_toggle = ActivedToggle.Field()
