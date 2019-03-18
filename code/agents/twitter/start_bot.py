import argparse
import json
import os
import random

import bots

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_agent",
                        help="User Agent to use. Defaults to a randomly selected one", default=None)
    parser.add_argument("--tor_proxy", help="HTTPS Proxy (to use with TOR)", default=None)
    parser.add_argument("--db_uri", help="URI of the database", default=None)
    parser.add_argument("--db_user", help="Username to use when authenticating with the database.",
                        default=None)
    parser.add_argument("--db_pass", help="Password to use when authenticating with the database.",
                        default=None)
    parser.add_argument("--bot",
                        help="Which bot type to use. Options: 1 - Twitter Bot (Default)",
                        type=int, default=1)
    # TODO add additional options?

    args = parser.parse_args()
    if args.user_agent is None:
        args.user_agent = random.choice(json.load(open("user_agents.json")))

    kwargs = {
            "user_agent": args.user_agent,
            "tor_proxy" : args.tor_proxy,
    }

    database_settings = None
    if args.db_uri is not None:
        if args.db_user is None or args.db_pass is None:
            raise ValueError("URI for the database present, but no authentication provided!")
        database_settings = {
                "uri"     : args.db_uri,
                "user"    : args.db_user,
                "password": args.db_pass
        }

    # Bot implementation
    if args.bot == 1:
        bot_class = bots.TwitterBot
        api_settings = {
                "consumer_key"       : os.environ["TWITTER_CONSUMER_KEY"],
                "consumer_secret"    : os.environ["TWITTER_CONSUMER_SECRET"],
                "access_token"       : os.environ["TWITTER_ACCESS_TOKEN"],
                "access_token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        }
    elif args.bot == 2:
        raise NotImplementedError(f"Bot {args.bot} isn't implemented!")
    else:
        raise NotImplementedError(f"Bot {args.bot} isn't implemented!")

    bot_instance = bot_class(**kwargs)
    bot_instance.connect_to_api(api=api_settings)
    bot_instance.connect_to_storage(database=database_settings)
    bot_instance.run()
