import pandas as pd
from cyberutils.graphql import execute_graphql

from config import GRAPHQL_URL, CYBER_ACCOUNT


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
    relevance_data = await execute_graphql(request=gql_query, graphql_url=GRAPHQL_URL)
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
    relevance_score_data = await execute_graphql(request=gql_query, graphql_url=GRAPHQL_URL)
    return relevance_score_data['relevance_leaderboard_aggregate']['nodes'][0]['share']
