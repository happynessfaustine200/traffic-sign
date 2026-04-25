from django.urls import path

from .views import detect_view, home, train_view

urlpatterns = [
    path("", home, name="home"),
    path("train/", train_view, name="train"),
    path("detect/", detect_view, name="detect"),
]
