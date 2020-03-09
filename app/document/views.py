""" views """
import os.path
# from django.forms.models import model_to_dict, fields_for_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File

from utils.parser.pdf import PdfParser
from utils.preprocessing.text import save_bag_of_words, prepare_coords
from .models import Document, PdfDocument
from .forms import DocumentForm

from utils.fusioncharts import FusionCharts
from collections import OrderedDict

dataSource = OrderedDict()

# The `chartConfig` dict contains key-value pairs data for chart attribute
chartConfig = OrderedDict()
chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
chartConfig["subCaption"] = "In MMbbl = One Million barrels"
chartConfig["xAxisName"] = "Country"
chartConfig["yAxisName"] = "Reserves (MMbbl)"
chartConfig["numberSuffix"] = "K"
chartConfig["theme"] = "fusion"

# The `chartData` dict contains key-value pairs data
chartData = OrderedDict()
chartData["Venezuela"] = 290
chartData["Saudi"] = 260
chartData["Canada"] = 180
chartData["Iran"] = 140
chartData["Russia"] = 115
chartData["UAE"] = 100
chartData["US"] = 30
chartData["China"] = 30

dataSource["chart"] = chartConfig
dataSource["data"] = []

# Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
# The data for the chart should be in an array wherein each element of the array is a JSON object
# having the `label` and `value` as keys.

# Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
for key, value in chartData.items():
  data = {}
  data["label"] = key
  data["value"] = value
  dataSource["data"].append(data)


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
    a_coord = prepare_coords(pdf.freq_items)
    column2D = FusionCharts("column2d", "ex1", "600", "400", "chart-1", "json",
                            dataSource)

    return render(
        request, 'document/document.html', {
            'doc': doc,
            'filename': filename,
            'file_ext': file_ext,
            'output': column2D.render(),
            'chartTitle': 'Simple Chart Using Array'
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
