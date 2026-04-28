from django.urls import path
from views import login_view, urlop_view, urlopomat_view

urlpatterns = [
    path('', urlop_view, name='urlop_dashboard'),       # Strona 1: urlop.html
    path('login/', login_view, name='login'),            # Strona 2: index.html
    path('panel/', urlopomat_view, name='urlopomat'),    # Strona 3: urlopomat.html
]