from django.urls import path
from views import login_view, urlop_view, urlopomat_view, wnioski_view, panel_admina_view

urlpatterns = [
    path('', urlop_view, name='urlop_dashboard'),           # Strona 1: urlop.html
    path('login/', login_view, name='login'),               # Strona 2: index.html
    path('panel/', urlopomat_view, name='urlopomat'),       # Strona 3: urlopomat.html
    path('wnioski/', wnioski_view, name='wnioski_page'),    # Strona 4: wniosek.html
    path('panel-admina/', panel_admina_view, name='panel_admina'), # Strona 5: panel.html
]