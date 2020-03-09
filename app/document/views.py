""" views """
import os.path
# from django.forms.models import model_to_dict, fields_for_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File

from utils.parser.pdf import PdfParser
from .models import Document, PdfDocument
from .forms import DocumentForm


@login_required(login_url='/accounts/login/')
def index(request):
  """ get document """
  return render(request, 'document/document.html')


@login_required(login_url='/accounts/login/')
def document(request, doc_id):
  """ get document by id """
  doc = get_object_or_404(Document, pk=doc_id)
  path, file_ext = os.path.splitext(doc.file.path)
  filename = os.path.basename(path)

  if request.GET.get('parser'):
    if not doc.is_parsed and file_ext == '.pdf':
      parser = PdfParser(doc.file.path)
      metadata = parser.extract_text()
      file_object = open('temp/parse_file/text.txt', 'rb')
      file = File(file_object)

      pdf = PdfDocument(doc=doc, metadata=metadata, text=file)
      pdf.save()

      doc.is_parsed = True
      doc.save()

  return render(request, 'document/document.html', {
      'doc': doc,
      'filename': filename,
      'file_ext': file_ext
  })


@login_required(login_url='/accounts/login/')
def upload_file(request):
  """ Upload file: html, pdf, docx """
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
