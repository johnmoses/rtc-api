import graphene
import datetime
from graphql_relay.node.node import from_global_id
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from .models import (
    Meeting
)
from .types import (
    MeetingType
)

class Query(graphene.ObjectType):
    meetings = DjangoFilterConnectionField(MeetingType, search=graphene.String())
    usermeetings = DjangoFilterConnectionField(MeetingType)

    meeting = graphene.relay.Node.Field(MeetingType)

    def resolve_meetings(root, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Meeting.objects.filter(filter)
        return Meeting.objects.all()


    def resolve_meeting(root, info, **kwargs):
        return Meeting.objects.get(id=kwargs.get('id'))


class MeetingCreate(graphene.Mutation):
    meeting = graphene.Field(MeetingType)

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        photo = graphene.String()
        scheduled_at = graphene.String()

    @classmethod
    def mutate(cls, _, info, name, description, photo, scheduled_at=None):
        starter = info.context.user
        _scheduled_at = None
        if scheduled_at != "":
            _scheduled_at = scheduled_at
        meeting = Meeting.objects.create(
            name=name,
            description=description,
            photo=photo,
            scheduled_at=_scheduled_at,
            starter=starter
        )
        meeting.save()
        return MeetingCreate(meeting=meeting)


class MeetingNameUpdate(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        name = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(
            pk=from_global_id(input.get('id'))[1])
        meeting.name = input.get('name')
        meeting.modified_at = datetime.datetime.now()
        meeting.save()
        return MeetingNameUpdate(meeting=meeting)

class MeetingDescriptionUpdate(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        description = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(
            pk=from_global_id(input.get('id'))[1])
        meeting.description = input.get('description')
        meeting.modified_at = datetime.datetime.now()
        meeting.save()
        return MeetingDescriptionUpdate(meeting=meeting)

class MeetingImageUpdate(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        photo = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(
            pk=from_global_id(input.get('id'))[1])
        meeting.photo = input.get('photo')
        meeting.modified_at = datetime.datetime.now()
        meeting.save()
        return MeetingImageUpdate(meeting=meeting)

class MeetingSchedule(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        scheduled_at = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(pk=from_global_id(input.get('id'))[1])

        meeting.scheduled_at = input.get('scheduled_at')
        meeting.save()
        return MeetingSchedule(meeting=meeting)

class MeetingStart(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        started_at = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(pk=from_global_id(input.get('id'))[1])

        meeting.started_at = datetime.datetime.now()
        meeting.save()
        return MeetingStart(meeting=meeting)

class MeetingEnd(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()
        video = graphene.String()
        ended_at = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(pk=from_global_id(input.get('id'))[1])

        meeting.video = input.get('ended_at')
        meeting.ended_at = datetime.datetime.now()
        meeting.save()
        return MeetingEnd(meeting=meeting)


class MeetingDelete(graphene.relay.ClientIDMutation):
    meeting = graphene.Field(MeetingType)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(self, info, **input):
        meeting = Meeting.objects.get(pk=from_global_id(input.get('id'))[1])
        meeting.is_deleted = True
        meeting.deleted_at = datetime.datetime.now()
        meeting.save()
        return MeetingDelete(meeting=meeting)


class Mutations(graphene.ObjectType):
    meeting_create = MeetingCreate.Field()
    meetingname_update = MeetingNameUpdate.Field()
    meetingdescription_update = MeetingDescriptionUpdate.Field()
    meetingimage_update = MeetingImageUpdate.Field()
    meeting_schedule = MeetingSchedule.Field()
    meeting_start = MeetingStart.Field()
    meeting_end = MeetingEnd.Field()
    meeting_delete = MeetingDelete.Field()
