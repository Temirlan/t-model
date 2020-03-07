from django.forms import ModelForm
from .models import Document
from django.utils.translation import gettext_lazy as _
from django import forms

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['author', 'name', 'file']
        help_texts = {
            'file': _("Allowed data types: 'html', 'pdf', 'docx'"),
        }

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author...'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name...'}),
            'file': forms.FileInput(attrs={'placeholder': 'Upload one file'}),
        }