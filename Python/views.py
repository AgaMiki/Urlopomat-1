from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == "agata@wp.pl" and password == "agata":  # Sprawdzenie poprawności danych logowania
            return redirect('urlop_dashboard') # Przekierowanie do widoku urlop_view po poprawnym logowaniu
        else:
            messages.error(request, "Nieprawidłowy e-mail lub hasło.")
            
    return render(request, 'login/index.html')

def urlop_view(request):
    return render(request, 'main/urlopomat.html') # Renderowanie szablonu urlopomat.html po zalogowaniu