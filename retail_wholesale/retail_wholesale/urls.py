from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from homepage.views import custom_403_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('retail/', include('retail.urls')),
    path('analysis/', include('analysis.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]

handler403 = custom_403_view
