from django.shortcuts import render


def index(request):
    template = 'homepage/index.html'
    return render(request, template)


def custom_403_view(request, exception):
    return render(request, 'core/403.html', {
        'message': str(exception)
    }, status=403)