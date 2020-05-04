import logging
from datetime import datetime
from django.db.models import Max, Count, Sum, Q
from api.models import *
import api.serializers as serializers
from api import neo4j
import json
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from api.queries_utils import paginator_factory, paginator_factory_non_queryset

logger = logging.getLogger('queries')


def next_id(model):
	max_id = model.objects.aggregate(Max('id'))['id__max']
	if not max_id:
		max_id = 0

	return max_id + 1


# -----------------------------------------------------------
# users
# -----------------------------------------------------------
def twitter_users_count():
	"""
	Returns: Number of  users saved on the mongo database wrapped on a dictionary
	"""
	try:
		all_users_count = User.objects.filter().count()
		return True, {'count': all_users_count}, "Success obtaining the number of users"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_count.__name__} -> {e}")
		return False, None, "Error obtaining the number of users"


def twitter_users(entries_per_page, page):
	"""
	Args:
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None
	Returns: Users saved on the mongo database wrapped on a dictionary divided per pages
	if entries_per_page and page are both None then all users will be returned
	"""
	try:
		all_users = User.objects.all()

		data = paginator_factory(all_users, entries_per_page, page)
		data['entries'] = [serializers.User(user).data for user in data['entries']]

		return True, data, "Success obtaining users info"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
		return False, None, f"Error obtaining users info"


def twitter_user(user_id):
	"""
	Args:
		user_id: User's ID

	Returns: User info defined by user_id parameter wrapped on a dictionary

	"""
	try:
		return True, serializers.User(
			User.objects.get(user_id=user_id)).data, f"Success obtaining user (id:{user_id})"

	except User.DoesNotExist as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user.__name__} -> {e}")
		return False, None, f"User (id:{user_id}) does not exists on database"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user.__name__} -> {e}")
		return False, None, f"Error obtaining user (id:{user_id})"


def twitter_users_stats(entries_per_page, page):
	"""

	Args:
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Stats saved on the postgres database wrapped on a dictionary divided per pages
	if entries_per_page and page are both None then all stats will be returned
	"""
	try:
		stats = UserStats.objects.all()

		data = paginator_factory(stats, entries_per_page, page)
		data['entries'] = [serializers.UserStats(us).data for us in data['entries']]

		return True, data, "Success obtaining users stats info"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
		return False, None, "Error obtaining users stats info"


def twitter_user_stats(user_id, entries_per_page, page):
	"""

	Args:
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's stats wrapped  on a dictionary divided per pages
	if entries_per_page and page are both None then all stats will be returned

	"""
	try:

		user_stats = UserStats.objects.filter(user_id=user_id)

		data = paginator_factory(user_stats, entries_per_page, page)
		data['entries'] = [serializers.UserStats(stat).data for stat in data['entries']]

		return True, data, f"Success obtaining user's (id:{user_id}) stats"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
		return False, None, f"Error obtaining user's (id:{user_id}) stats"


def twitter_user_stats_grouped(user_id, types):
	"""

	Args:
		user_id: User's ID
		types: Group labels (day,month,year)

	Returns: User's stats  grouped by (day or month or year) wrapped on dictionary

	"""
	try:
		start_date = UserStats.objects.filter(user_id=user_id).order_by('timestamp').values('timestamp')[0]['timestamp']

		query = "UserStats.objects.filter(user_id=user_id)"
		for group_type in types:
			query += f".annotate({group_type}=Extract{group_type.title()}('timestamp'))"

		order_by_list = [f"'{group_type}'" for group_type in types]
		query += f".values({','.join(order_by_list)}).annotate(sum_followers=Sum('followers'), sum_following=Sum('following')).order_by({','.join(order_by_list)})"

		users_stats = []
		for obj in list(eval(query)):
			full_date = '/'.join(str(obj.pop(group_type)) for group_type in types)
			obj['full_date'] = full_date
			users_stats.append(obj)

		return True, {'data': users_stats, 'start_date': start_date}, \
			   f"Success obtaining user's (id:{user_id}) stats grouped"

	except Exception as e:
		logger.error(
			f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats_grouped.__name__} -> {e}")
		return False, None, f"Error obtaining user's (id:{user_id}) stats grouped"


def twitter_user_tweets(user_id, entries_per_page, page):
	"""

	Args:
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's tweets wrapped  on a dictionary divided per pages
	if entries_per_page and page are both None then all tweets will be returned

	"""
	try:
		user_tweets = Tweet.objects.filter(user=user_id).order_by('-created_at')

		data = paginator_factory(user_tweets, entries_per_page, page)
		data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

		return True, data, f"Success obtaining user's (id:{user_id}) tweets"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
		return False, None, f"Error obtaining user's (id:{user_id}) tweets"


def twitter_user_followers(user_id, entries_per_page, page):
	"""

	Args:
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's followers wrapped  on a dictionary divided per pages
	if entries_per_page and page are both None then all followers will be returned

	"""
	try:
		followers = neo4j.get_followers({'id': user_id})

		data = paginator_factory_non_queryset(followers, entries_per_page, page)

		return True, data, f"Success obtaining users's (id:{user_id}) followers"

	except Exception as e:
		logger.error(
			f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_followers.__name__} -> {e}")
		return False, None, f"Error obtaining users's (id:{user_id}) followers"


def twitter_user_following(user_id, entries_per_page, page):
	"""

	Args:
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's following wrapped  on a dictionary divided per pages
	if entries_per_page and page are both None then all following will be returned

	"""
	try:
		following = neo4j.get_following({'id': user_id})

		data = paginator_factory_non_queryset(following, entries_per_page, page)

		return True, data, f"Success obtaining users's (id:{user_id}) following"

	except Exception as e:
		logger.error(
			f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_following.__name__} -> {e}")
		return False, None, f"Error obtaining users's (id:{user_id}) following"


def twitter_search_users(keywords, entries_per_page, page):
	"""

	Args:
		keywords: Words to be searched
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's  that matches keywords on name and screen_name wrapped on response's object divided by pages
	if entries_per_page and page are both None then all users will be returned

	"""
	try:
		query_filters = Q()
		for word in keywords.split():
			query_filters |= Q(name__icontains=word) | Q(screen_name__icontains=word)

		users = User.objects.filter(query_filters)

		data = paginator_factory(users, entries_per_page, page)
		data['entries'] = [serializers.User(user).data for user in data['entries']]

		return True, data, f"Success searching users by {keywords}"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_search_users.__name__} -> {e}")
		return False, None, f"Error searching users by {keywords}"


def twitter_users_type(user_id):
	"""
	Args:
		user_id: User's ID

	Returns: User's type wrapped on dictionary

	"""
	try:
		node_type = neo4j.node_type({'id': user_id})
		return True, {'type': node_type}, f"Success obtaining user's (id:{user_id}) type"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_type.__name__} -> {e}")
		return False, None, f"Error obtaining user's (id:{user_id}) type"


# -----------------------------------------------------------
# tweets
# -----------------------------------------------------------

def twitter_tweets(entries_per_page, page):
	"""

	Args:
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All tweets saved on databases wrapped on dictionary divided by pages
	if entries_per_page and page are both None then all tweets will be returned
	"""
	try:
		all_tweets = Tweet.objects.all()

		data = paginator_factory(all_tweets, entries_per_page, page)
		data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

		return True, data, "Success obtaining tweets"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
		return False, None, "Error obtaining tweets"


def twitter_tweets_stats(entries_per_page, page):
	"""

	Args:
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All tweets stats saved on databases wrapped on dictionary divided by pages
	if entries_per_page and page are both None then all tweets stats will be returned

	"""
	try:
		tweet_stats = TweetStats.objects.all()

		data = paginator_factory(tweet_stats, entries_per_page, page)
		data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']]

		return True, data, "Success obtaining tweets stats"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets_stats.__name__} -> {e}")
		return False, None, "Error obtaining tweets stats"


def twitter_tweet(tweet_id):
	"""

	Args:
		tweet_id: Tweet's ID

	Returns: Tweet info wrapped  on response's dictionary

	"""
	try:

		return True, serializers.Tweet(Tweet.objects.get(tweet_id=tweet_id)).data, \
			   f"Success obtaining tweet's (id:{tweet_id}) info"

	except Tweet.DoesNotExist as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet.__name__} -> {e}")
		return False, None, f"Tweet (id:{tweet_id}) does not exist on database"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet.__name__} -> {e}")
		return False, None, f"Error obtaining tweet's (id:{tweet_id}) info"


def twitter_tweet_stats(tweet_id, entries_per_page, page):
	"""

	Args:
		tweet_id: Tweet's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Tweet's stats wrapped on dictionary divided by pages
	if entries_per_page and page are both None then tweet's stats will be returned
	"""
	try:
		stats = TweetStats.objects.filter(tweet_id=tweet_id).order_by('-timestamp')

		data = paginator_factory(stats, entries_per_page, page)
		data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']]

		return True, data, f"Success obtaining tweet's (id:{tweet_id}) stats"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
		return False, None, f"Error obtaining tweet's (id:{tweet_id} stats"


def twitter_tweet_replies(tweet_id):
	"""

	Args:
		tweet_id: Tweet's ID

	Returns: Tweet's replies wrapped on dictionary

	"""
	try:
		all_tweets = Tweet.objects.filter(in_reply_to_status_id=tweet_id)

		return True, [serializers.Tweet(tweet).data for tweet in
					  all_tweets], f"Success obtaining all tweet's (id:{tweet_id}) replies"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: "
					 f"Function {twitter_tweet_replies.__name__} -> {e}")
		return False, None, f"Error obtaining all tweet's (id:{tweet_id}) replies"


# -----------------------------------------------------------
# policies
# -----------------------------------------------------------

def policy(policy_id):
	"""

	Args:
		policy_id:  Policy's ID

	Returns: Policy's info  wrapped on  dictionary

	"""
	try:
		policy_by_id = Policy.objects.get(id=policy_id)
		return True, serializers.Policy(policy_by_id).data, f"Success obtaining policy's (id:{policy_id}) info"

	except Policy.DoesNotExist as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy.__name__} -> {e}")
		return False, None, f"Policy (id:{policy_id}) does not exist on database"
	except Exception as e:

		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy.__name__} -> {e}")
		return False, None, f"Error obtaining policy's (id:{policy_id}) info"


def policies(entries_per_page, page):
	"""

	Args:
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All policies saved wrapped on dictionary divided in pages
	if entries_per_page and page are both None then all policies will be returned
	"""
	try:
		all_policies = Policy.objects.all()

		data = paginator_factory(all_policies, entries_per_page, page)
		data['entries'] = [serializers.Policy(policy_obj).data for policy_obj in data['entries']]
		for entry in data['entries']:
			for index in range(len(entry['bots'])):
				bot_id = entry['bots'][index]
				user_obj = User.objects.filter(user_id=bot_id)
				bot_name = user_obj[0].screen_name if len(user_obj) > 0 else ''
				entry['bots'][index] = {"bot_id": bot_id, "bot_name": bot_name}

		return True, data, "Success obtaining all policies"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policies.__name__} -> {e}")
		return False, None, "Error obtaining all policies"


def bot_policies(bot_id, entries_per_page, page):
	"""

	Args:
		bot_id: Bot's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Bot assigned policies wrapped on dictionary divided in pages
	if entries_per_page and page are both None then all bots will be returned
	"""
	try:
		policies_list = Policy.objects.filter(bots__contains=[bot_id])

		data = paginator_factory(policies_list, entries_per_page, page)
		data['entries'] = [serializers.Policy(policy_obj).data for policy_obj in data['entries']]

		return True, data, f"Success obtaining bot's (id:{bot_id}) policy info"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {bot_policies.__name__} -> {e}")
		return False, None, f"Error obtaining bot's (id:{bot_id}) policy info"


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
			return False, policy_serializer.errors, "Invalid data"

		for bot_id in policy_serializer.data['bots']:
			if not neo4j.check_bot_exists(str(bot_id)):
				raise AddPolicyError("Invalid Bot's ID")

		status = Policy.objects.filter(API_type=policy_serializer.data['API_type'],
									   filter=policy_serializer.data['filter'],
									   tags=policy_serializer.data['tags']).exists()
		if status:
			args = {"API_type": policy_serializer.data['API_type'],
					"filter": policy_serializer.data['filter'],
					"tags": policy_serializer.data['tags']}

			raise AddPolicyError(f"A policy with similar arguments (args: {args}) is already on database ")

		policy = Policy.objects.create(id=next_id(Policy), **policy_serializer.data)

		return True, {'id': policy.id}, "Success adding a new policy"

	except AddPolicyError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
		return False, None, str(e)
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
		return False, None, "Error adding a new policy"


def remove_policy(policy_id):
	"""

	Args:
		policy_id:  Policy's ID

	Returns: Remove operation status wrapped on dictionary

	"""
	try:
		Policy.objects.get(id=policy_id).delete()
		return True, None, f"Successful policy  (id:{policy_id}) removal"

	except Policy.DoesNotExist:
		return False, None, f"Policy (id:{policy_id}) does not exist on database"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {remove_policy.__name__} -> {e}")
		return False, None, f"Error policy  (id:{policy_id}) removal"


def update_policy(data, policy_id):
	"""

	Args:
		data: Dictionary with data to be updated
		policy_id: Policy's ID

	Returns: Update operation status wrapped on dictionary

	"""
	try:
		policy_obj = Policy.objects.get(id=policy_id)
		data = dict([(key, value) for key, value in data.items() if key != 'id'])
		policy_obj.__dict__.update(data)
		policy_obj.save()

		return True, serializers.Policy(policy_obj).data, f"Success in updating the policy (id:{policy_id})"

	except Policy.DoesNotExist as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
		return False, None, f"Policy (id:{policy_id}) does not exists on database"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
		return False, None, f"Error in updating the policy (id:{policy_id})"


# Bots
def twitter_bot_logs(bot_id, entries_per_page, page):
	"""
	
	Args:
		bot_id: Bots's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns:  Bot's logs wrapped on dictionary divided by pages
	if entries_per_page and page are both None then all logs will be returned

	"""
	try:
		logs = Log.objects.filter(id_bot=bot_id).order_by('-timestamp')

		data = paginator_factory(logs, entries_per_page, page)
		data['entries'] = [serializers.Log(log).data for log in data['entries']]

		for entry in data['entries']:
			target_id = entry['target_id']
			user_obj = User.objects.filter(user_id=target_id)
			entry['target_screen_name'] = user_obj[0].screen_name if len(user_obj) > 0 else ''

		return True, data, f"Success obtaining bot's (id:{bot_id}) logs"

	except ValueError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
		return False, None, f"Error obtaining bot's (id:{bot_id}) logs"


def twitter_bot(bot_id):
	"""

	Args:
		bot_id: Bot's ID

	Returns: Bot's info wrapped on dictionary

	"""
	try:
		if not neo4j.check_bot_exists(bot_id):
			return False, None, f"Bot (id:{bot_id}) does not exist on database"

		return True, serializers.User(User.objects.get(user_id=int(bot_id))).data, \
			   f"Success obtaining bot's (id:{bot_id}) info"

	except User.DoesNotExist as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot.__name__} -> {e}")
		return False, None, f"Bot (id:{bot_id}) does not exist on both database"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot.__name__} -> {e}")
		return False, None, f"Error obtaining bot's (id:{bot_id}) info"


def twitter_bots():
	"""

	Returns: All bots's info saved on database wrapped on dictionary

	"""
	try:
		bots_ids = [int(bot['id']) for bot in neo4j.search_bots()]

		data = [serializers.User(user).data for user in User.objects.filter(user_id__in=bots_ids)]

		return True, data, "Success obtaining bots's info"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bots.__name__} -> {e}")
		return False, None, "Error obtaining bots's info"


def twitter_bot_messages(bot_id):
	"""

	Args:
		bot_id: Bots'ID

	Returns:

	"""
	try:
		data = [serializers.Message(msg).data for msg in Message.objects.filter(bot_id=bot_id)]
		return True, data, f"Success obtaining bot's (id:{bot_id}) direct messages"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_messages.__name__} -> {e}")
		return False, None, f"Error obtaining bot's (id:{bot_id}) direct messages"


# Network
def twitter_sub_network(queries):
	"""

	Args:
		queries:  Array of neo4j queries

	Returns: Neo4'j sub network in json format wrapped on response's object

	"""
	try:
		data = []
		for query in queries:
			data += [entry['result'] for entry in neo4j.export_query(query)]

		return True, data, "Success obtaining a network defined by a query"

	except AttributeError as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
		return False, None, str(e)

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
		return False, None, "Error obtaining a network defined by a query"


def twitter_network():
	"""

	Returns:  Neo4'j network in json format wrapped on dictionary

	"""

	try:
		data = neo4j.export_network("json")
		return True, data, f"Success obtaining full network"

	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_network.__name__} -> {e}")
		return False, None, f"Error obtaining full network"
