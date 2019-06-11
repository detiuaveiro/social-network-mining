from django.urls import path, include
from rest_framework import routers

import app.views as views
import app.viewsets as viewsets

app_name = "app"


# Needed to avoid problems with CORS
class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


rest_routes = OptionalSlashRouter()
rest_routes.register("images", viewsets.ImageViewSet, basename="images")

api_routes = rest_routes.urls + [

]
urlpatterns = [
    path('api/', include(api_routes)),
    path('images/', views.images, name="images_view"),
    path('images/<int:image_id>/', views.get_image_by_id, name="images_view_id"),
    path('images/<int:image_id>/rate', views.rate_image, name="rate_image"),
]
