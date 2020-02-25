from django.db import models
from django.conf import settings


class Question(models.Model):
    """
    Question model.
    Slug field is generated pre-save using signal.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='questions')

    def __str__(self):
        return self.content[:30]


class Answer(models.Model):
    """
    Answer model. Field 'voters' is used to store up likes.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    question = models.ForeignKey(Question,
                                  on_delete=models.CASCADE,
                                  related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='votes')

    def __str__(self):
        return self.author.username
