from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import FileResponse
from rest_framework.status import *
from report.report_gen import Report
from django.core.files.base import ContentFile
import json


@api_view(["POST"])
def create_report(request):
	"""
	Args:
		request: HTTP Request
	Returns: Create a new Report based on Request
	"""

	report = Report()

	result = report.create_report(request.data['match'], params=request.data['fields'], limit=request.data['limit'])
	result_json = json.dumps(result)
	file_to_send = ContentFile(result_json)
	response = HttpResponse(file_to_send, content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response['Content-Length'] = file_to_send.size
	response['Content-Disposition'] = 'attachment; filename=report.json'
	return response
