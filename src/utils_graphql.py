import pandas as pd
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from config import GRAPHQL_URL, CYBER_ACCOUNT


async def execute_graphql(gql_query,
                          gql_url=GRAPHQL_URL):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=gql_url)
    # Create a GraphQL client using the defined transport
    async with Client(
        transport=transport, fetch_schema_from_transport=True,
    ) as session:
        # Execute single query
        query = gql(gql_query)
        return await session.execute(query)


async def get_relevance(height):
    gql_query = \
        """
        query GetRelevance {{
          relevance_aggregate(order_by: {{rank: desc}}, where: {{height: {{_eq: {}}}}}) {{
            nodes {{
              object
              rank
              id
              height
            }}
          }}
        }}
        """.format(height)
    relevance_data = await execute_graphql(gql_query)
    return pd.DataFrame(relevance_data['relevance_aggregate']['nodes'])


async def get_relevance_score(cyber_account=CYBER_ACCOUNT):
    gql_query = \
        """
        query GetRelevanceScore {{
          relevance_leaderboard_aggregate(where: {{subject: {{_eq: "{}"}}}}) {{
            nodes {{
              share
            }}
          }}
        }}
        """.format(cyber_account)
    relevance_score_data = await execute_graphql(gql_query)
    return relevance_score_data['relevance_leaderboard_aggregate']['nodes'][0]['share']
