import graphene
import graphql_jwt

import api.accounts.schema
import api.analytics.schema
import api.meetings.schema


class Query(
    api.accounts.schema.Query,
    api.analytics.schema.Query,
    api.meetings.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    api.accounts.schema.Mutations,
    api.analytics.schema.Mutations,
    api.meetings.schema.Mutations,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()

    delete_refresh_token_cookie = \
        graphql_jwt.relay.DeleteRefreshTokenCookie.Field()


schema = graphene.Schema(
    query=Query, 
    mutation=Mutation, 
)
