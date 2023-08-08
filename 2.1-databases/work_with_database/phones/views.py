from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_type = request.GET.get("sort", None)
    sort_types = {
        'name': Phone.objects.order_by('name'),
        'min_price': Phone.objects.order_by('price'),
        'max_price': Phone.objects.order_by('-price'),
        'release_date': Phone.objects.order_by('-release_date'),
        None: Phone.objects.all(),
    }
    context = {"phones": sort_types[sort_type]}
    template = 'catalog.html'
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]
    context = {"phone": phone}
    return render(request, template, context)
