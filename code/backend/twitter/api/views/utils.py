from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


NETWORK_QUERY = "MATCH r=() - [] -> ()  RETURN r LIMIT 750"


def create_response(data=None, success_messages=None, error_messages=None, status=HTTP_200_OK):
	return Response({
		"data": data,
		"success_messages": success_messages,
		"error_messages": error_messages,
	}, status=status)


def nodes_label_choice(show_bots, show_users):
	if not show_bots and not show_users:
		return "false"

	types_clause = [clause for clause in ['entity2:Bot' if show_bots else '', 'entity2:User' if show_users else '']
					if clause != '']

	return ' or '.join(types_clause)


def args_validator(ids_list, depth_list, label):
	depth = []

	if len(depth_list) > 1:
		if len(ids_list) != len(depth_list):
			raise ValueError(f"{label}_id and {label}_depth should have same amount of arguments or "
							 f"{label}_depth = <integer>")
	elif len(depth_list) == 1:
		depth = [depth_list[0] for _ in range(len(ids_list))]
	else:
		depth = [0 for _ in range(len(ids_list))]

	return depth


def queries_generator(ids_list, depth_list, show_bots, show_users, label):
	queries = []

	for i in range(len(ids_list)):
		_id = ids_list[i]
		_depth = depth_list[i]
		query = f"match result=(entity1:{label} {{ id : {_id} }})-[:FOLLOWS*0..{_depth}]->(entity2) where " \
				f"{nodes_label_choice(show_bots, show_users)} return result"

		queries.append(query)

	return queries


def cypher_query_generator(request_params):
	show_bots = bool(int(request_params.get('show_bots', '1')))
	show_users = bool(int(request_params.get('show_users', '1')))

	bots_id = [f"'{i}'" for i in request_params.getlist('bots_id', [])]
	bots_depth = args_validator(bots_id, request_params.getlist('bots_depth', []), "bots")
	bot_queries = queries_generator(bots_id, bots_depth, show_bots, show_users, "Bot")

	users_id = [int(i) for i in request_params.getlist('users_id', [])]
	users_depth = args_validator(users_id, request_params.getlist('users_depth', []), "users")
	user_queries = queries_generator(users_id, users_depth, show_bots, show_users, "User")

	if len(bots_id + users_id) == 0:
		return [f"match result=()-[]-(entity2) where {nodes_label_choice(show_bots, show_users)} return result"]

	return list(set(bot_queries + user_queries))
