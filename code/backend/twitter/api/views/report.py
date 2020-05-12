from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.status import *
from report.report_gen import Report
from django.core.files.base import ContentFile
import os


@api_view(["POST"])
def create_report(request):
	"""
	Args:
		request: HTTP Request
	Returns: Create a new Report based on Request
	"""

	report = Report()
	print(request.data)
	match = {
		"start": request.data["start"],
		"intermediates": request.data["intermediate"],
		"end": request.data["end"]
	}

	export = request.data['fileType']

	file = report.create_report(match=match, params=request.data['fields'], limit=request.data['limit'], export=export)
	with open(file, "r") as file_reader:
		result = file_reader.read()
	os.remove(file)
	file_to_send = ContentFile(result)
	response = HttpResponse(file_to_send, content_type='application/' + export)
	response['Content-Length'] = file_to_send.size
	response['Content-Disposition'] = 'attachment; filename=report.' + export
	return response
