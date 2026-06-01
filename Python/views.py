import calendar
from django.shortcuts import render, redirect
from django.contrib import messages

def urlop_view(request):
    cal = calendar.HTMLCalendar(firstweekday=0)
    html_kalendarz = cal.formatmonth(2026, 6)
    
    html_kalendarz = html_kalendarz.replace(
        '<table border="0" cellpadding="0" cellspacing="0" class="month">',
        '<table class="table table-bordered table-striped text-center mt-2">'
    )
    
    context = {
        'kalendarz': html_kalendarz
    }
    return render(request, 'web/urlop.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == "agata@wp.pl" and password == "agata":
            return redirect('urlopomat') 
        else:
            messages.error(request, "Nieprawidłowy e-mail lub hasło.")
            
    return render(request, 'login/index.html')

def urlopomat_view(request):
    # Czyste renderowanie strony 3, bez żadnych ukrytych przekierowań
    return render(request, 'urlopomat/urlopomat.html')

def wnioski_view(request):
    # Renderowanie szablonu wnioski.html z folderu wnioski
    return render(request, 'wnioski/wniosek.html')