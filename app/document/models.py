from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_file_extension

User = get_user_model()

# Create your models here.
class Document(models.Model):
    author = models.CharField("author", max_length=100)
    name = models.CharField("name", max_length=250)
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE)
    created = models.DateTimeField("created", auto_now_add=True, null=True)
    file = models.FileField(upload_to="media/files/%Y/%m/%d", validators=[validate_file_extension], max_length=600)
    
class PdfDocument(models.Model):
    doc = models.ForeignKey(Document, verbose_name="document", on_delete=models.CASCADE)