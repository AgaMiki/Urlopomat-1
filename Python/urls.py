from django.urls import path
from views import login_view, urlop_view 

urlpatterns = [
    path('', login_view, name='login'), # Strona logowania
    path('urlop/', urlop_view, name='urlop_dashboard'), # Strona docelowa po zalogowaniu
]