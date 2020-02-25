from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api.views import (QuestionViewSet,
                                 AnswerCreateAPIView,
                                 QuestionAnswerListAPIView,
                                 AnswerRUDAPIView,
                                 AnswerLikeAPIView)


router = DefaultRouter()

router.register(r'questions', QuestionViewSet)
urlpatterns = [
    path('', include(router.urls)),

    path('questions/<slug:slug>/answer/',
         AnswerCreateAPIView.as_view(),
         name='answer-create'),

    path('questions/<slug:slug>/answers/',
         QuestionAnswerListAPIView.as_view(),
         name='list-question-answers'),

    path('answers/<int:pk>/',
         AnswerRUDAPIView.as_view(),
         name='list-question-detail'),

    path('answers/<int:pk>/like/',
         AnswerLikeAPIView.as_view(),
         name='answer-like'),
]
