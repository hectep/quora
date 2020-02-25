from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from questions.models import Answer, Question
from questions.api.serializers import QuestionSerializer, AnswerSerializer
from questions.api.permissions import IsAuthorOrReadOnly


class QuestionViewSet(ModelViewSet):
    """
    Viewset for question model
    """
    queryset = Question.objects.all().order_by('-created_at')
    lookup_field = 'slug'
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

    def perform_create(self, serializer):
        """
        We need to fill up author field on creation.
        """
        serializer.save(author=self.request.user)


class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        """
        Filling the author and related question fields for an answer
        """
        user = self.request.user
        kwarg_slug = self.kwargs.get('slug')
        question = get_object_or_404(Question, slug=kwarg_slug)
        if question.answers.filter(author=user).exists():
            raise ValidationError('You have already answered that question')
        serializer.save(question=question, author=self.request.user)


class QuestionAnswerListAPIView(generics.ListAPIView):
    """
    API view to fetch all answerss related to certain question
    """
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        kwarg_slug = self.kwargs.get('slug')
        return Answer.objects.filter(
            question__slug=kwarg_slug).order_by('-created_at')


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Standard RUD for original authors of an answer
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)


class AnswerLikeAPIView(APIView):
    """
    API view for like button implementation.
    Likes are using m2m field of an answer model linking it with Profile model
    """
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, )

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


