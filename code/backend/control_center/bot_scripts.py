import os
import sys
import argparse
import Enums.enums as enums
from send import RabbitSend


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        help="Location of the Rabbit host. Defaults to localhost",
                        default="127.0.0.1")
    parser.add_argument("-p","--port",
                        help="Port of the Rabbit Host. Defaults to 5672",
                        default=5672, type=int)
    parser.add_argument("-v","--vhost",
                        help="Rabbit Virtual Host. Defaults to PI",
                        default="PI")
    parser.add_argument("-U","--user",
                    help="Username for rabbit", required=True)
    parser.add_argument("-P","--password",
                    help="Password for rabbit", required=True)
    parser.add_argument("-x","--xchange",
                help="Name of the exchange to send to", required=True)
    parser.add_argument("-r","--rt_key",
                help="Prefix for the routing key", required=True)
    parser.add_argument("-t","--task",
                help="Task to send", required=True, type=int)
    parser.add_argument("-at","--arg_type",
            help="DEPRECATED. Only used for 2 of the tasks (find followers and follow users)")
    parser.add_argument("-a","--args",
            help="Arguments for the task", required=True, nargs="+")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()

    # trying to get the enum, for validation purposes
    task_type = args.task
    enum_value_map = { enums.ResponseTypes.__members__[m].value : enums.ResponseTypes.__members__[m] for m in enums.ResponseTypes.__members__}

    try:
        task_type = enum_value_map[task_type]
    except KeyError:
        print("Unknown Task value provided!")
        print("List of available tasks: ")
        for i in enums.ResponseTypes:
            print(i)
        sys.exit(1)

    # Creating the rabbit connection
    conn = RabbitSend(host=args.host, port=args.port, vhost=args.vhost,
                               username=args.user,
                               password=args.password)
    print("Data read with arg_type <{}> and args <{}>".format(args.arg_type, args.args))
    print("Sending to Exchange <{}> with routing_key <{}>...".format(args.xchange, args.rt_key))
    payload = {
        "type" : task_type,
    }
    if args.arg_type:
        params = {
            "type" : args.arg_type,
            "data" : args.args
        }
    else:
        params = args.args[0]
        # handling Ids being passed
        try:
            params = int(params)
        except ValueError:
            # ignore if string (though generally shouldn't happen)
            pass

    payload["params"] = params
    conn.send(routing_key=args.rt_key, message=payload)
    conn.close()