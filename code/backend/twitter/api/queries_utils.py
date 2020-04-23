from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginator_factory(query_data, entries_per_page, page):
	entries_per_page = int(entries_per_page) if entries_per_page is not None else len(query_data)
	page = int(page) if page is not None else 1

	data = {}

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
