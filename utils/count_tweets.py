import pandas as pd
import requests
import os
import json
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': '#ETH', 'granularity': 'hour'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()



def tweet_count(query_params):
    json_response = connect_to_endpoint(query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    df = pd.DataFrame(json_response['data'])
    print(df)
    df = df[['start', 'end', 'tweet_count']]
    df[['start', 'end']] = df[['start', 'end']].applymap(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M'))
    return df





