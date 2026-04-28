from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == "agata@wp.pl" and password == "agata":
            # Po poprawnym zalogowaniu idziesz na stronę 3
            return redirect('urlopomat') 
        else:
            messages.error(request, "Nieprawidłowy e-mail lub hasło.")
            
    return render(request, 'login/index.html')
def urlop_view(request):
    # Teraz to jest strona główna (z napisem "Witaj")
    return render(request, 'web/urlop.html')

def urlopomat_view(request):
    return render(request, 'urlopomat/urlopomat.html') # Renderowanie szablonu urlopomat.html po zalogowaniu