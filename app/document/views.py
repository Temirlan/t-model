""" views """
import os.path

# from django.forms.models import model_to_dict, fields_for_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from utils.fusioncharts import FusionCharts

from utils.parser.pdf import PdfParser
from utils.preprocessing.text import save_bag_of_words, prepare_coords
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

  if doc.is_parsed:
    pdf = PdfDocument.objects.get(doc_id=doc.id)
    data_source = prepare_coords(pdf.freq_items, doc.name)
    bar_chart = FusionCharts("bar2d", "ex1", "600", "400", "chart-1", "json",
                             data_source)

    return render(
        request, 'document/document.html', {
            'doc': doc,
            'pdf': pdf,
            'filename': filename,
            'file_ext': file_ext,
            'output': bar_chart.render(),
            'count_words': len(pdf.freq_items)
        })

  if request.GET.get('parser'):
    if not doc.is_parsed and file_ext == '.pdf':
      parser = PdfParser(doc.file.path)
      metadata = parser.extract_text()
      freq_items = save_bag_of_words('temp/parse_file/text.txt')

      file_object = open('temp/preprocessing/bag_of_words.txt', 'rb')
      file = File(file_object)

      pdf = PdfDocument(doc=doc,
                        metadata=metadata,
                        text=file,
                        freq_items=list(freq_items))
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
