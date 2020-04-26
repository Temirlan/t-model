""" views """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from document.models import Document, PdfDocument
from django.forms.models import model_to_dict, fields_for_model
from utils.preprocessing.text import create_thematic_model

from .models import ThematicModel


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
    phi_tau = float(request.POST.get('phi_tau') or 0)
    theta_tau = float(request.POST.get('theta_tau') or 0)
    decorr_tau = float(request.POST.get('decorr_tau') or 0)

    if not num_topics or not num_tokens or not phi_tau or not theta_tau or not decorr_tau:
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
      perplexity_score, sparsity_phi_score, sparsity_theta_score, topic_dictionary = create_thematic_model(
          checked_list, num_topics, num_tokens, phi_tau, theta_tau, decorr_tau)

      model = ThematicModel(perplexity_score=perplexity_score,
                            sparsity_phi_score=sparsity_phi_score,
                            sparsity_theta_score=sparsity_theta_score,
                            topic_dictionary=topic_dictionary,
                            user_id=request.user.id)
      model.save()
      model.pdf_docs.add(*checked_list)
      model.save()

      return redirect('tmodel', model.id)

    else:
      is_checked_files = False

  return render(request, 'tmodel/tmodel-create.html', {
      'list': pdf_list,
      'is_checked_files': is_checked_files,
  })


@login_required(login_url='/accounts/login/')
def tmodel(request, t_id):
  """ get document by id """
  t_model = get_object_or_404(ThematicModel, pk=t_id)

  return render(request, 'tmodel/tmodel.html', {'t_model': t_model})
