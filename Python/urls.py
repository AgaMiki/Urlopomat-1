from django.urls import path
from views import login_view, budget_view

urlpatterns = [
    path('', login_view, name='login'),
    path('budget/', budget_view, name='budget'),
]