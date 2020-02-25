from django.urls import path

from profiles.api.views import CurrentProfileAPIView


urlpatterns = [
    path('profile/', CurrentProfileAPIView.as_view(), name='current-profile'),
]
