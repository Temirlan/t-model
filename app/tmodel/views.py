from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from document.models import Document, PdfDocument
from django.forms.models import model_to_dict, fields_for_model
from utils.preprocessing.text import create_thematic_model


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
  """ create a thematic model """
  is_checked_files = True
  is_filled_fields = True
  pdf_list = PdfDocument.objects.all()

  if request.method == 'POST':
    checked_ids = []
    num_topics = int(request.POST.get('num_topics') or 0)
    num_tokens = int(request.POST.get('num_tokens') or 0)
    phi_tau = int(request.POST.get('phi_tau') or 0)
    theta_tau = int(request.POST.get('theta_tau') or 0)
    decorr_tau = int(request.POST.get('decorr_tau') or 0)

    if not num_topics or not num_topics or not phi_tau or not theta_tau or not decorr_tau:
      is_filled_fields = False

      return render(request, 'tmodel/tmodel.html', {
          'list': pdf_list,
          'is_filled_fields': is_filled_fields
      })

    for item in pdf_list:
      if request.POST.get(str(item.id), 'off') in 'on':
        checked_ids.append(item.id)

    if len(checked_ids) != 0:
      checked_list = pdf_list.filter(pk__in=checked_ids)
      # create_thematic_model(checked_list)
    else:
      is_checked_files = False

  return render(request, 'tmodel/tmodel.html', {
      'list': pdf_list,
      'is_checked_files': is_checked_files,
  })
