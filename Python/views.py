from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Uwierzytelnienie - pamiętaj, że username w Django to zazwyczaj nazwa użytkownika, 
        # a nie e-mail. Jeśli chcesz logować e-mailem, sprawdź czy model User jest do tego dostosowany.
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('budget') # Przekierowanie do panelu urlopowego
        else:
            messages.error(request, "Nieprawidłowy e-mail lub hasło.")
            
    return render(request, 'login/index.html')

def budget_view(request):
    # Widok panelu budżetu/urlopy
    return render(request, 'budget/index.html')