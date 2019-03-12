from django.shortcuts import render, redirect, get_object_or_404
from app.models import Image
import random


# Create your views here.

def home(request):
    random_image_id = random.randint(1, Image.objects.count())

    return redirect('image_by_id', image_id=random_image_id)


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
            # otherwise ignore
        return redirect('home')
    else:
        return redirect('home')
