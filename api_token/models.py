from django.db import models
from django.contrib.auth import get_user_model


class Token(models.Model):
    """APIトークン"""
    token = models.CharField('トークン', max_length=255)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
