from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from document.models import Document

@login_required(login_url='/accounts/login/')
def index(request):
    lists = Document.objects.all()
    
    paginator = Paginator(lists, 10)

    page = request.GET.get('page')
    try:
        aPaginator = paginator.page(page)
    except PageNotAnInteger:
        aPaginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        aPaginator = paginator.page(paginator.num_pages)
    
    return render(request, 'documents/documents.html', {"aPaginator": aPaginator})