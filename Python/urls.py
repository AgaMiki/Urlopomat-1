from django.urls import path
# Pamiętaj o dopisaniu wnioski_view do importu!
from views import login_view, urlop_view, urlopomat_view, wnioski_view 

urlpatterns = [
    path('', urlop_view, name='urlop_dashboard'),        # Strona 1: urlop.html
    path('login/', login_view, name='login'),             # Strona 2: index.html
    path('panel/', urlopomat_view, name='urlopomat'),     # Strona 3: urlopomat.html
    path('wnioski/', wnioski_view, name='wnioski_page'),   # NOWA Strona 4: wnioski.html
]