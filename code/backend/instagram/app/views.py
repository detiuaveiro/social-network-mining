import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app import utils
from app.models import Image


# Create your views here.
@csrf_exempt
def images(request):
    try:
        random_image_id = random.randint(1, Image.objects.count())
        return redirect('app:images_view_id', image_id=random_image_id)
    except ValueError:
        return render(request, 'home.html', {})


def get_image_by_id(request, image_id: int):
    image = utils.get_object_by_pk(Image, pk=image_id)
    context = {}
    if image is not None:
        context["image"] = image
    return render(request, 'home.html', context)


def rate_image(request, image_id: int):
    if request.method == 'POST':
        image = Image.objects.get(pk=image_id)
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
        return redirect('app:images_view')
    else:
        return redirect('app:images_view')
