from django.shortcuts import render
from django.http import HttpResponse
from superstocks.models import State,City,SuperStokist,Village
from django.core.paginator import Paginator
from rest_framework import viewsets
from superstocks.serializers import SuperstockistSerializer

def home(request):
    obj=list(superstocks.objects.all())
    return render(request,'home.html',{'object':obj})

def index(request):
    return render(request, 'superstocks/index.html')


def listing(request):
    contact_list = Village.objects.all()
    paginator = Paginator(contact_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})

class SuperstockistViewSet(viewsets.ModelViewSet):
    queryset = SuperStokist.objects.all()
    serializer_class = SuperstockistSerializer