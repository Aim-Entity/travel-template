from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("videos", views.VideoViewSet)
router.register("ratings", views.RatingViewSet)
router.register("users", views.UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index")
]