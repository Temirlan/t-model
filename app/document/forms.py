""" Forms """
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Document


class DocumentForm(ModelForm):
  """ Form model document """
  class Meta:  # pylint: disable=too-few-public-methods
    """ Model Document """
    model = Document
    fields = ['author', 'name', 'file']
    help_texts = {
        'file': _("Allowed data types: 'html', 'pdf', 'docx'"),
    }

    widgets = {
        'author':
        forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author...'
        }),
        'name':
        forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter name...'
        }),
        'file':
        forms.FileInput(attrs={'placeholder': 'Upload one file'}),
    }
