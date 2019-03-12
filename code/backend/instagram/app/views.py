from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Image
from django.shortcuts import HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def images(request):
    if request.method == "GET":
        random_image_id = random.randint(1, Image.objects.count())
        return redirect('image_by_id', image_id=random_image_id)
    elif request.method == "POST":
        return add_image(request)


def add_image(request):
    if request.method == 'POST':
        if request.FILES["file"]:
            image = Image.objects.create(file=request.FILES["file"])
            image.save()
            return HttpResponse(status=204)
        return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def get_image_by_id(request, image_id: int):
    if Image.objects.count() == 0:
        context = {}
    else:
        context = {
            "image": Image.objects.get(id=image_id)
        }
    return render(request, 'home.html', context)


def rate_image(request, image_id: int):
    if request.method == 'POST':
        image = Image.objects.get(id=image_id)
        data = request.POST
        # if there is a vote, add to the total
        if data["vote"]:
            image.total_voted += 1
            value = data["vote"]
            # if it was yes
            if value == "1":
                image.total_score += 1
            image.save()
            # otherwise ignore
        return redirect('images')
    else:
        return redirect('images')
