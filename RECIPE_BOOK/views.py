from django.shortcuts import render

def handler400(request, exception):
    """
    Custom 400 page
    """
    context = {
        'page_title': '400'
    }
    return render(request, "errors/400.html", context, status=400)

def handler403(request, exception):
    """
    Custom 403 page
    """
    context = {
        'page_title': '403'
    }
    return render(request, "errors/403.html", context, status=403)

def handler404(request, exception):
    """
    Custom 404 page
    """
    context = {
        'page_title': '404'
    }
    return render(request, "errors/404.html", context, status=404)

def handler500(request):
    """
    Custom 500 page
    """
    context = {
        'page_title': '500'
    }
    return render(request, "errors/500.html", context, status=500)