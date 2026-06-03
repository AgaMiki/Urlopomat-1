import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Pracownik, Wnioski 

# ==========================================================================
# Funkcja: login_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Obsługuje proces logowania użytkownika. Dla żądania POST pobiera 
#          login oraz hasło, weryfikuje istnienie pracownika w bazie, sprawdza
#          status aktywności konta oraz poprawność hasła. W przypadku sukcesu
#          zapisuje ID pracownika w sesji. Dla żądania GET wyświetla formularz.
# Zwraca: HttpResponse - przekierowanie do panelu głównego ('urlopomat') 
#         w przypadku sukcesu lub renderowanie szablonu strony logowania z błędami.
# ==========================================================================
def login_view(request):
    if request.method == 'POST':
        wpisany_login = request.POST.get('email') 
        wpisane_haslo = request.POST.get('password')
        
        try:
            pracownik = Pracownik.objects.get(login=wpisany_login)
            
            if not pracownik.czy_aktywny:
                messages.error(request, "To konto jest nieaktywne.")
                return render(request, 'login/index.html')

            if pracownik.sprawdz_haslo(wpisane_haslo):
                request.session['pracownik_id'] = pracownik.id
                return redirect('urlopomat')
            else:
                messages.error(request, "Nieprawidłowe hasło.")
                
        except Pracownik.DoesNotExist:
            messages.error(request, "Nieprawidłowy login (e-mail).")
            
    return render(request, 'login/index.html')


# ==========================================================================
# Funkcja: urlop_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Generuje publiczną stronę główną systemu. Wykorzystuje wbudowaną
#          bibliotekę Pythona 'calendar' do wygenerowania surowego kalendarza
#          HTML dla wybranego miesiąca (Czerwiec 2026).
# Zwraca: HttpResponse - wyrenderowany szablon strony startowej ('web/urlop.html')
#         wraz ze zmienną 'kalendarz' przekazaną do kontekstu.
# ==========================================================================
def urlop_view(request):
    cal = calendar.HTMLCalendar(firstweekday=0)
    html_kalendarz = cal.formatmonth(2026, 6)
    return render(request, 'web/urlop.html', {'kalendarz': html_kalendarz})


# ==========================================================================
# Funkcja: urlopomat_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Obsługuje prywatny panel składania wniosków urlopowych. Sprawdza
#          czy użytkownik jest uwierzytelniony w sesji. Jeśli otrzyma żądanie
#          POST, pobiera wybrane daty startu/końca urlopu i zapisuje w bazie
#          nowy wniosek ze statusem "oczekujacy".
# Zwraca: HttpResponse - przekierowanie do listy wniosków ('wnioski_page') 
#         po udanym zapisie formularza lub wyrenderowany widok panelu głównego
#         ('urlopomat/urlopomat.html') z danymi zalogowanego pracownika.
# ==========================================================================
def urlopomat_view(request):
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login')

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


# ==========================================================================
# Funkcja: wnioski_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Obsługuje podgląd oraz modyfikację statusów wniosków. Weryfikuje sesję.
#          1. Jeśli żądanie to POST, a użytkownik jest adminem, zmienia status
#             wniosku na zaakceptowany (i odejmuje dni z puli pracownika) lub odrzucony.
#          2. Przy żądaniu GET pobiera zestaw danych: dla admina wszystkie wnioski
#             w systemie, dla zwykłego pracownika wyłącznie jego własne (sortowane od najnowszych).
# Zwraca: HttpResponse - przekierowanie odświeżające stronę ('wnioski_page') po
#         podjęciu decyzji przez admina lub wyrenderowaną stronę z tabelą
#         ('wnioski/wniosek.html') zawierającą listę wniosków i obiekt pracownika.
# ==========================================================================
def wnioski_view(request):
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login')

    pracownik = Pracownik.objects.get(id=pracownik_id)
    
    if request.method == 'POST' and pracownik.czy_admin:
        wniosek_id = request.POST.get('wniosek_id')
        akcja = request.POST.get('akcja')
        
        wniosek = get_object_or_404(Wnioski, id=wniosek_id)
        
        if akcja == 'zaakceptuj':
            wniosek.status = 'zaakceptowany'
            dni = (wniosek.data_do - wniosek.data_od).days + 1
            wniosek.skladajacy.dostepne_dni -= dni
            wniosek.skladajacy.save()
        elif akcja == 'odrzuc':
            wniosek.status = 'odrzucony'
            
        wniosek.rozpatrujacy = pracownik
        wniosek.save()
        return redirect('wnioski_page')

    if pracownik.czy_admin:
        lista_wnioskow = Wnioski.objects.all().order_by('-id')
    else:
        lista_wnioskow = Wnioski.objects.filter(skladajacy=pracownik).order_by('-id')

    context = {
        'wnioski': lista_wnioskow,
        'pracownik': pracownik
    }
    return render(request, 'wnioski/wniosek.html', context)