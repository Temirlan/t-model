""" Create your models here. """
from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_file_extension

USER = get_user_model()


class Document(models.Model):
  """ Model Document """
  author = models.CharField("author", max_length=100)
  name = models.CharField("name", max_length=250)
  user = models.ForeignKey(USER, verbose_name="user", on_delete=models.CASCADE)
  created = models.DateTimeField("created", auto_now_add=True, null=True)
  file = models.FileField(upload_to="media/files/%Y/%m/%d",
                          validators=[validate_file_extension],
                          max_length=600)


class PdfDocument(models.Model):
  """ Model PdfDocument """
  doc = models.ForeignKey(Document,
                          verbose_name="document",
                          on_delete=models.CASCADE)
