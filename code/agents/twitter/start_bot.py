import argparse
import os
import bots
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_agent",
                        help="User Agent to use. Defaults to a randomly selected one",
                        default=os.environ.get("USER_AGENT", None))
    parser.add_argument("--tor_proxy",
                        help="HTTPS Proxy (to use with TOR)",
                        default=os.environ.get("TOR_PROXY", None))
    parser.add_argument("--server_host", help="Location of the server",
                        default=os.environ.get("SERVER_HOST", None))
    parser.add_argument("--server_port", help="Port the server is listening to",
                        default=os.environ.get("SERVER_PORT", None))
    parser.add_argument("--bot",
                        help="Which bot type to use. Options: 1 - Twitter Bot (Default)",
                        type=int, default=1)
    # TODO add additional options?
    args = parser.parse_args()
    params = vars(args)
    if any(params[arg] is None for arg in params):
        print("The following arguments are required:", file=sys.stderr)
        print("\n".join(arg for arg in params if params[arg] is None), file=sys.stderr)
        exit(-1)
    kwargs = {
        "user_agent": args.user_agent,
        "tor_proxy" : args.tor_proxy,
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
    bot_instance.run()
