import logging
from datetime import datetime
from django.db.models import Max, Q
from api.models import *
import api.serializers as serializers
from api import neo4j
import json

from api.queries_utils import paginator_factory

logger = logging.getLogger('queries')


def next_id(model):
	max_id = model.objects.aggregate(Max('id'))['id__max']
	if not max_id:
		max_id = 0

	return max_id + 1


# -----------------------------------------------------------
# users
# -----------------------------------------------------------


def twitter_users(entries_per_page, page):
	try:
		all_users = User.objects.filter()

		data = paginator_factory(all_users, entries_per_page, page)
		data['entries'] = [serializers.User(user).data for user in data['entries']]

		return True, data, "Sucesso a obter todos os utilizadores"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
		return False, None, f"Erro a obter todos os utilizadores"


def twitter_user(id):
	try:
		return True, serializers.User(User.objects.get(user_id=id)).data, "Sucesso o utilizador pedido"
	except User.DoesNotExist:
		return False, None, f"O utilizador de id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user.__name__} -> {e}")
		return False, None, f"Erro a obter o utilizador de id {id}"


def twitter_users_stats(entries_per_page, page):
	try:

		stats = UserStats.objects.all()
		data = paginator_factory(stats, entries_per_page, page)

		data['entries'] = [serializers.UserStats(us).data for us in data['entries']]

		return True, data, "Sucesso a obter as estatisticas de todos os utilizadores"
	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
		return False, None, f"Erro as estatisticas de todos os utilizadores"


def twitter_user_stats(id, entries_per_page, page):
	try:

		user_stats = UserStats.objects.filter(user_id=id)
		data = paginator_factory(user_stats, entries_per_page, page)

		data['entries'] = [serializers.UserStats(stat).data for stat in data['entries']]

		return True, data, "Sucesso a obter as estatisticas do utilizador pedido"
	except UserStats.DoesNotExist:
		return False, None, f"Não existe nenhum utilizador com o id {id} na base de dados de estatisticas"
	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
		return False, None, f"Erro as estatisticas do utilizador de id {id}"


def twitter_user_tweets(id, entries_per_page, page):
	try:
		user_tweets = Tweet.objects.filter(user=id).order_by('-created_at')

		data = paginator_factory(user_tweets, entries_per_page, page)
		data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

		return True, data, "Sucesso a obter todos os tweets do utilizador pedido"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
		return False, None, f"Erro a obter os tweets do utilizador de id {id}"


def twitter_user_followers(id):
	try:
		followers = neo4j.get_followers({'id': id})
		if not followers:
			return False, None, f"Não existem followers do utilizador de id {id} na base de dados"
		return True, followers, "Sucesso a obter todos os followers do utilizador pedido"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
		return False, None, f"Erro a obter os followers do utilizador de id {id}"


def twitter_user_following(id):
	try:
		following = neo4j.get_following({'id': id})
		if not following:
			return False, None, f"Não existem  utilizadores a serem seguidos pelo utilizador de id {id} na base de dados"
		return True, following, "Sucesso a obter todos os utilizadores que o utilizador pedido segue"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
		return False, None, f"Erro a obter os utilizadores que o utilizador de id {id} segue"


def twitter_search_users(keywords):
	try:
		query_filters = Q()
		for word in keywords.split():
			query_filters |= Q(name__icontains=word) | Q(screen_name__icontains=word)
			
		users = User.objects.filter(query_filters)

		return True, [serializers.User(user).data for user in users], "Sucesso a efetuar a pesquisa de utilizadores"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
		return False, None, f"Erro a efetuar a pesquisa de utilizadores"


# -----------------------------------------------------------
# tweets
# -----------------------------------------------------------

def twitter_tweets(entries_per_page, page):
	try:
		all_tweets = Tweet.objects.all()

		data = paginator_factory(all_tweets, entries_per_page, page)
		data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

		return True, data, "Sucesso a obter todos os tweets"
	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
		return False, None, "Erro a obter todos os tweets"


def twitter_tweets_stats(entries_per_page, page):
	try:
		tweet_stats = TweetStats.objects.all()

		data = paginator_factory(tweet_stats, entries_per_page, page)
		data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']]

		return True, data, "Sucesso a obter as estatisticas de todos os tweets"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, "Erro a obter as estatisticas de todos os tweets"


def twitter_tweet(id):
	try:
		Tweet.objects.get(tweet_id=id)
		all_tweets = Tweet.objects.filter(tweet_id=id)
		return True, [serializers.Tweet(tweet).data for tweet in all_tweets], "Sucesso a obter todos os tweets"
	except Tweet.DoesNotExist:
		return False, None, f"O id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet.__name__} -> {e}")
		return False, None, f"Erro a obter todos os tweets do id {id}"


def twitter_tweet_stats(id, entries_per_page, page):
	try:
		stats = TweetStats.objects.filter(tweet_id=id).order_by('-timestamp')
		data = paginator_factory(stats, entries_per_page, page)
		data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']],

		return True, data, "Sucesso a obter as estatisticas do tweet de id pedido"
	except TweetStats.DoesNotExist:
		return False, None, f"Não existem estatísticas do tweet de id {id} na base de dados"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, f"Erro a obter as estatisticas do tweet de id {id}"


def twitter_tweet_replies(id):
	try:
		Tweet.objects.get(in_reply_to_status_id=id)
		all_tweets = Tweet.objects.filter(in_reply_to_status_id=id)
		return True, [serializers.Tweet(tweet).data for tweet in
					  all_tweets], "Sucesso a obter todas as replies ao tweet"
	except Tweet.DoesNotExist:
		return False, None, f"Não existem replies ao tweet de id {id}"
	except Exception as e:
		logger.error(
			f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_replies.__name__} -> {e}")
		return False, None, f"Erro a obter todas as replies do tweet de id {id}"


# -----------------------------------------------------------
# policies
# -----------------------------------------------------------

def policy(id):
	"""
	Get a policy by ID saved in DB
	:param id: policy id
	:return: sstatus(boolean), data, message(string)
	"""
	try:
		policy_by_id = Policy.objects.get(id=id)
		return True, serializers.Policy(policy_by_id).data, "Sucesso a obter a politica"
	except Policy.DoesNotExist:
		return False, None, f"O id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy.__name__} -> {e}")
		return False, None, "Erro a obter a politica"


def policies():
	"""
	Get all availables policies saved on DB
	:return: status(boolean), data, message(string)
	"""
	try:
		all_policies = Policy.objects.all()
		data = [serializers.Policy(policy).data for policy in all_policies]
		return True, data, "Sucesso a obter todas as politicas"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policies.__name__} -> {e}")
		return False, None, "Erro a obter todas as politicas"


def bot_policies(id):
	"""
	Get all availables policies by bot's id saved on DB
	:return: status(boolean), data, message(string)
	"""
	try:
		policies = Policy.objects.filter(bots__contains=[id])
		data = [serializers.Policy(policy).data for policy in policies]
		return True, data, f"Sucesso a obter as politicas do bot {id}"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {bot_policies.__name__} -> {e}")
		return False, None, f"Erro a obter as politicas do bot {id}"


def add_policy(data):
	"""
	Add new policy to DB
	:param data: Dictionary with data to be inserted
		Items:
			- id : int
			- API_type : str
			- filter : str
			- name : str
			- tags : str[]
			- bots : int[]
		Ex: { "API_type": "Twitter", "filter": "Instagram", "name": "Politica", "tags": ["PSD", "CDS"], "bots": [1, 2] }
	:return: status(boolean), data, message(string)
	"""

	class AddPolicyError(Exception):
		pass

	try:
		policy_serializer = serializers.Policy(data=data)
		if not policy_serializer.is_valid():
			return False, policy_serializer.errors, "Dados invalidos!"

		for bot_id in policy_serializer.data['bots']:
			if not neo4j.check_bot_exists(bot_id):
				raise AddPolicyError("IDs dos bots invalidos")

		status = Policy.objects.filter(API_type=policy_serializer.data['API_type'],
									   filter=policy_serializer.data['filter'],
									   tags=policy_serializer.data['tags']).exists()
		if status:
			args = {"API_type": policy_serializer.data['API_type'],
					"filter": policy_serializer.data['filter'],
					"tags": policy_serializer.data['tags']}

			raise AddPolicyError(f"Uma politica com argumentos iguais já existe na base de dados. Args: {args}")

		policy = Policy.objects.create(id=next_id(Policy), **policy_serializer.data)

		return True, {'id': policy.id}, "Sucesso a adicionar uma nova politica"

	except AddPolicyError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
		return False, None, str(e)
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
		return False, None, f"Erro ao adicionar uma nova politica->{e}"


def remove_policy(id):
	"""
	Remove a policy by ID saved in DB
	:param id: policy id
	:return: status(boolean), data, message(string)
	"""
	try:
		Policy.objects.get(id=id).delete()
		return True, None, f"Sucesso a eliminar a politica com ID {id}"
	except Policy.DoesNotExist:
		return False, None, f"O id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {remove_policy.__name__} -> {e}")
		return False, None, f"Erro a eliminar a politica com ID {id}"


def update_policy(data, id):
	"""
	Update a policy by ID saved in DB
	:param id: policy id
	:return: status(boolean), data, message(string)
	"""
	try:
		policy = Policy.objects.get(id=id)
		data = dict([(key, value) for key, value in data.items() if key != 'id'])
		policy.__dict__.update(data)
		policy.save()
		return True, None, f"Sucesso a editar a politica com ID {id}"
	except Policy.DoesNotExist:
		return False, None, f"O id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
		return False, None, f"Erro a editar  a politica com ID {id}"


def policy_by_service(service):
	"""
	Return all service policies saved in DB
	:param id: service name
	:return: status(boolean), data, message(string)
	"""
	try:
		data = [serializers.Policy(policy).data for policy in Policy.objects.filter(API_type=service)]
		return True, data, f"Sucesso a obter as politicas do {service}"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy_by_service.__name__} -> {e}")
		return False, None, f"Erro a obter as politicas do {service}"


def twitter_bot_logs(id, entries_per_page, page):
	"""
	Return all logs from a bot
	:param id: bot id
	:param limit: number of logs
	:return: status(boolean), data, message(string)
	"""
	try:
		logs = Log.objects.filter(id_bot=id).order_by('-timestamp')

		data = paginator_factory(logs, entries_per_page, page)

		data['entries'] = [serializers.Log(log).data for log in data['entries']]

		return True, data, f"Sucesso a obter os logs do bot com ID {id}"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
		return False, None, f"Erro a obter os logs do bot com ID {id}"


# Bots

def twitter_bot(id):
	"""
	Return data associated to a bot , defined by his id
	:param id: bot's id
	:return: status(boolean), data, message(string)
	"""
	try:
		if not neo4j.check_bot_exists(id):
			return False, None, f"Bot com id {id} não existe na base de dados"
		bot = neo4j.search_bots({"id": id})

		return True, bot, f"Sucesso a obter informações do bot com ID {id}"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot.__name__} -> {e}")
		return False, None, f"Erro a obter as informações do bot com ID {id}"


def twitter_bots():
	"""
	Return all bots info saved on mongodb
	:return: status(boolean), data, message(string)
	"""
	try:
		bots_ids = [int(bot['id']) for bot in neo4j.search_bots()]
		data = [serializers.User(user).data for user in User.objects.filter(user_id__in=bots_ids)]

		return True, data, f"Sucesso a obter a informação de todos os bots"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bots.__name__} -> {e}")
		return False, None, "Erro a obter a informação de todos os bots"


def twitter_bot_messages(id):
	"""
	Return all privates messages from a bot
	:param id: id's bot
	:return: status(boolean), data, message(string)
	"""
	try:
		data = [serializers.Message(msg).data for msg in Message.objects.filter(bot_id=id)]
		return True, data, f"Sucesso a obter as mensagens privadas dos bot com id {id}"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_messages.__name__} -> {e}")
		return False, None, f"Erro a obter as mensagens privadas dos bot com id {id}"


# Network
def twitter_sub_network(queries):
	"""
	Return a subgraph defined by queries clause
	Args:
		queries:  list of query clauses

	Returns:

	"""
	try:
		data = []
		for query in queries:
			data += [entry['result'] for entry in neo4j.export_query(query)]

		return True, data, "Subgrafo da rede obtido com sucesso"
	except AttributeError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
		return False, None, str(e)
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
		return False, None, "Erro ao obter um sub-grafo da rede"


def twitter_network():
	"""
	Returns neo4j full network
	Returns: status(boolean), data, message(string)
	"""

	try:
		data = json.loads(neo4j.export_network("json"))
		return True, data, f"Sucesso a obter os dados da rede"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_network.__name__} -> {e}")
		return False, None, f"Erro a obter os dados da rede"
