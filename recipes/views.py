from django.shortcuts import render
from .models import Recipe

def home(request):

    template = "index.html"
    context = {
        "page_title": "Home"
    }

    return render(request, template, context)
