from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import math
import datetime


def paginator_factory(query_data, entries_per_page, page):
	entries_per_page = int(entries_per_page) if entries_per_page is not None else query_data.count()
	page = int(page) if page is not None else 1

	data = {}
	if query_data.count() == 0:
		entries_per_page = 1

	if entries_per_page > 0:
		paginator = None

		try:
			paginator = Paginator(query_data, entries_per_page)
			data['entries'] = paginator.page(page)
		except PageNotAnInteger:
			data['entries'] = paginator.page(1)
			page = 1

		except EmptyPage:
			data['entries'] = paginator.page(paginator.num_pages)
			page = paginator.num_pages

		data['num_pages'] = paginator.num_pages
		data['next_page'] = page + 1 if page + 1 <= paginator.num_pages else 1
		data['previous_page'] = page - 1 if page - 1 > 0 else paginator.num_pages

	else:
		raise ValueError("Invalid value for entries_per_page parameter. Should be greater than 0")

	return data


def paginator_factory_non_queryset(query_data, entries_per_page, page):
	entries_per_page = int(entries_per_page) if entries_per_page is not None else len(query_data)
	page = int(page) if page is not None else 1

	if len(query_data) == 0:
		entries_per_page = 1

	num_pages = math.ceil(len(query_data) / entries_per_page)

	start = (page - 1) * entries_per_page
	end = start + entries_per_page

	data = {
		'entries': query_data[start:end],
		'num_pages': num_pages,
		'next_page': page + 1 if page + 1 <= num_pages else 1,
		'previous_page': page - 1 if page - 1 > 0 else num_pages
	}

	return data


def convert_policy(policy):
	policy['bots'] = [str(bot) for bot in policy['bots']]
	return policy
