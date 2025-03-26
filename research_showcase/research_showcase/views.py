from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")

def search_page(request):
    return render(request, 'search.html')
