import calendar
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Pracownik, Wnioski # Import modeli z bazy danych

def login_view(request):
    if request.method == 'POST':
        # Pobieramy dane z formularza (w HTML input ma name="email")
        wpisany_login = request.POST.get('email') 
        wpisane_haslo = request.POST.get('password')
        
        try:
            # Szukamy pracownika w bazie po loginie
            pracownik = Pracownik.objects.get(login=wpisany_login)
            
            # Sprawdzamy czy konto jest aktywne
            if not pracownik.czy_aktywny:
                messages.error(request, "To konto jest nieaktywne.")
                return render(request, 'login/index.html')

            # Sprawdzamy hasło (zakładam, że model ma metodę sprawdzającą, np. sprawdz_haslo)
            # Jeśli w modelu hasło jest czystym tekstem, zmień na: pracownik.haslo == wpisane_haslo
            if hasattr(pracownik, 'sprawdz_haslo') and pracownik.sprawdz_haslo(wpisane_haslo):
                haslo_poprawne = True
            else:
                # Awaryjne sprawdzenie, jeśli hasła w bazie nie są hashowane
                haslo_poprawne = (pracownik.haslo == wpisane_haslo)

            if haslo_poprawne:
                # Zapisujemy ID zalogowanego pracownika w sesji przeglądarki
                request.session['pracownik_id'] = pracownik.id
                return redirect('urlopomat')
            else:
                messages.error(request, "Nieprawidłowe hasło.")
                
        except Pracownik.DoesNotExist:
            messages.error(request, "Nieprawidłowy login (e-mail).")
            
    return render(request, 'login/index.html')


def urlop_view(request):
    cal = calendar.HTMLCalendar(firstweekday=0)
    html_kalendarz = cal.formatmonth(2026, 6)
    html_kalendarz = html_kalendarz.replace(
        '<table border="0" cellpadding="0" cellspacing="0" class="month">',
        '<table class="table table-bordered table-striped text-center mt-2">'
    )
    return render(request, 'web/urlop.html', {'kalendarz': html_kalendarz})


def urlopomat_view(request):
    # Sprawdzamy, czy użytkownik jest zalogowany (czy istnieje w sesji)
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login') # Jeśli nie, wyrzucamy na stronę logowania

    pracownik = Pracownik.objects.get(id=pracownik_id)

    if request.method == 'POST':
        data_start = request.POST.get('data_start')
        data_end = request.POST.get('data_end')
        
       
        Wnioski.objects.create(
            skladajacy=pracownik,
            data_od=data_start,
            data_do=data_end,
            status="oczekujacy"
        )
        messages.success(request, "Wniosek został wysłany.")
        return redirect('wnioski_page')

    return render(request, 'urlopomat/urlopomat.html', {'pracownik': pracownik})

def wnioski_view(request):
    # Sprawdzamy autoryzację
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login')

    pracownik = Pracownik.objects.get(id=pracownik_id)
    
    # Pobieramy z bazy SQL tylko wnioski tego konkretnego pracownika
    moje_wnioski = Wnioski.objects.filter(skladajacy=pracownik)

    # POPRAWIONE: Wyrównane wcięcie (4 spacje) oraz właściwa nazwa pliku wniosek.html
    return render(request, 'wnioski/wniosek.html', {'wnioski': moje_wnioski})