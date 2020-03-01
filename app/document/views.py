from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Document, PdfDocument
from .forms import DocumentForm

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'document/document.html')

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