from django.urls import path
from blog.views import SearchAPIView


urlpatterns = [
    path("", SearchAPIView.as_view())
]
