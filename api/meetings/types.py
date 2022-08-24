from graphene import Connection, Node, Int
from graphene_django.types import DjangoObjectType
from .models import (
    Meeting
)


class MeetingConnection(Connection):
    class Meta:
        abstract = True
    count = Int()

    def resolve_count(root, info):
        return len(root.edges)


class MeetingType(DjangoObjectType):
    class Meta:
        model = Meeting
        filter_fields = {
            'id': ['exact', 'icontains'],
            'name': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'starter': ['exact'],
            'starter_id': ['exact'],
            'is_deleted': ['exact', 'icontains'],
        }
        interfaces = (Node, )
        connection_class = MeetingConnection

