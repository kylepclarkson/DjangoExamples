from django.shortcuts import render


# render index template for React
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')
