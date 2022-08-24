import graphene
from graphql_relay.node.node import from_global_id
from graphene_django.filter import DjangoFilterConnectionField
from .models import (
    Analytic
)
from .types import (
    AnalyticType
)


class Query(graphene.ObjectType):
    analytics = DjangoFilterConnectionField(AnalyticType)

    analytic = graphene.relay.Node.Field(AnalyticType)

    def resolve_analytics(root, info, **kwargs):
        return Analytic.objects.all()

    def resolve_analytic(root, info, **kwargs):
        return Analytic.objects.get(id=kwargs.get('id'))

class AnalyticCreate(graphene.relay.ClientIDMutation):
    analytic = graphene.Field(AnalyticType)

    class Input:
        anonymous_id = graphene.String()
        title = graphene.String()
        event = graphene.String()
        channel = graphene.String()
        category = graphene.String()
        resource = graphene.String()
        url = graphene.String()
        path = graphene.String()
        user_id = graphene.String()
        method = graphene.String()
        response_time = graphene.String()
        day = graphene.String()
        hour = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        analytic = Analytic(
            anonymous_id=input.get('anonymous_id'),
            title=input.get('title'),
            event=input.get('event'),
            channel=input.get('channel'),
            category=input.get('category'),
            resource=input.get('resource'),
            url=input.get('url'),
            path=input.get('path'),
            user_id=input.get('user_id'),
            method=input.get('method'),
            response_time=input.get('response_time'),
            day=input.get('day'),
            hour=input.get('hour'),
        )
        analytic.save()
        return AnalyticCreate(analytic=analytic)

class AnalyticUpsert(graphene.relay.ClientIDMutation):
    analytic = graphene.Field(AnalyticType)

    class Input:
        id = graphene.ID()
        anonymous_id = graphene.String()
        title = graphene.String()
        event = graphene.String()
        channel = graphene.String()
        category = graphene.String()
        resource = graphene.String()
        url = graphene.String()
        path = graphene.String()
        user_id = graphene.String()
        method = graphene.String()
        response_time = graphene.String()
        day = graphene.String()
        hour = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        analytic = Analytic(
            id=input.get('id'),
            anonymous_id=input.get('anonymous_id'),
            title=input.get('title'),
            event=input.get('event'),
            channel=input.get('channel'),
            category=input.get('category'),
            resource=input.get('resource'),
            url=input.get('url'),
            path=input.get('path'),
            user_id=input.get('user_id'),
            method=input.get('method'),
            response_time=input.get('response_time'),
            day=input.get('day'),
            hour=input.get('hour'),
        )
        analytic.save()
        return AnalyticUpsert(analytic=analytic)


class AnalyticUpdate(graphene.relay.ClientIDMutation):
    analytic = graphene.Field(AnalyticType)

    class Input:
        id = graphene.ID()
        anonymous_id = graphene.String()
        title = graphene.String()
        event = graphene.String()
        channel = graphene.String()
        category = graphene.String()
        resource = graphene.String()
        url = graphene.String()
        path = graphene.String()
        user_id = graphene.String()
        method = graphene.String()
        response_time = graphene.String()
        day = graphene.String()
        hour = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        analytic = Analytic.objects.get(
            pk=from_global_id(input.get('id'))[1])
        analytic.anonymous_id = input.get('anonymous_id')
        analytic.title = input.get('title')
        analytic.event = input.get('event')
        analytic.channel = input.get('channel')
        analytic.category = input.get('category')
        analytic.resource = input.get('resource'),
        analytic.url = input.get('url')
        analytic.path = input.get('path')
        analytic.user_id = input.get('user_id')
        analytic.method = input.get('method')
        analytic.response_time = input.get('response_time')
        analytic.day = input.get('day')
        analytic.hour = input.get('hour')
        analytic.save()

        return AnalyticUpdate(analytic=analytic)


class Mutations(graphene.ObjectType):
    analytic_create = AnalyticCreate.Field()
    analytic_upsert = AnalyticUpsert.Field()
    analytic_update = AnalyticUpdate.Field()
