from django.urls import path
from .views import autocomplete, home

urlpatterns = [
    path('', home, name='home'),
    path('autocomplete', autocomplete, name='autocomplete'),

]
