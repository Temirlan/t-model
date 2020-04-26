""" Create your models here. """
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from document.models import PdfDocument

USER = get_user_model()


class ThematicModel(models.Model):
  """ Model ThematicModel """
  user = models.ForeignKey(USER, verbose_name="user", on_delete=models.CASCADE)
  created = models.DateTimeField("created", auto_now_add=True, null=True)
  perplexity_score = models.FloatField("perplexity_score")
  sparsity_phi_score = models.FloatField("sparsity_phi_score")
  sparsity_theta_score = models.FloatField("sparsity_theta_score")
  topic_dictionary = JSONField(default=dict)
  pdf_docs = models.ManyToManyField(PdfDocument)
