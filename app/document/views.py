from django.forms.models import model_to_dict, fields_for_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import os.path

from .models import Document, PdfDocument
from .forms import DocumentForm

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'document/document.html')

@login_required(login_url='/accounts/login/')
def document(request, id):
    doc = get_object_or_404(Document, pk=id)
    path, file_ext = os.path.splitext(doc.file.path)
    filename = os.path.basename(path)
    
    return render(request,
     'document/document.html',
     {
        'doc': doc, 
        'filename': filename,
        'file_ext': file_ext
     })

@login_required(login_url='/accounts/login/')
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('/documents')
    else:
        form = DocumentForm()

    return render(request, 'document/upload_file.html', {'form': form})