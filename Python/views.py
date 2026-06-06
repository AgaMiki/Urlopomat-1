import calendar, random
from datetime import datetime,date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Pracownik, Wnioski 
from django.db.models import Count
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
# Co robi: Generuje publiczną stronę główną systemu. Dynamicznie pobiera 
#          aktualną datę systemową, generuje kalendarz dla bieżącego miesiąca
#          i roku, a następnie automatycznie lokalizuje i podświetla w kodzie 
#          HTML dzisiejszy dzień (np. 4 czerwca 2026).
# Zwraca: HttpResponse - wyrenderowany szablon strony startowej ('web/urlop.html')
#          wraz ze zmienną 'kalendarz' przekazaną do kontekstu.
# ==========================================================================
def urlop_view(request):
    dzisiaj = date.today()
    aktualny_rok = dzisiaj.year
    aktualny_miesiac = dzisiaj.month
    aktualny_dzien = dzisiaj.day

    cal = calendar.HTMLCalendar(firstweekday=0)
    html_kalendarz = cal.formatmonth(aktualny_rok, aktualny_miesiac)
    
    szukana_komorka = f'<td>{aktualny_dzien}</td>'
    podmieniona_komorka = f'<td><span class="dzisiaj">{aktualny_dzien}</span></td>'
    
    html_kalendarz = html_kalendarz.replace(szukana_komorka, podmieniona_komorka)
    
    return render(request, 'web/urlop.html', {'kalendarz': html_kalendarz})

# ==========================================================================
# Funkcja: urlopomat_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Obsługuje prywatny panel składania wniosków urlopowych. Sprawdza
#          czy użytkownik jest zalogowany. Przy POST pobiera daty oraz informację
#          czy urlop ma być płatny. Weryfikuje poprawność chronologiczną dat.
#          Jeśli wybrano urlop płatny, wylicza dni i blokuje wysłanie wniosku,
#          jeśli pracownik przekracza swój limit dostępnych dni urlopowych.
# Zwraca: HttpResponse - przekierowanie do listy wniosków ('wnioski_page') 
#         po udanym zapisie lub ponowne wyrenderowanie panelu z komunikatem błędu.
# ==========================================================================
def urlopomat_view(request):
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login')

    pracownik = Pracownik.objects.get(id=pracownik_id)

    if request.method == 'POST':
        data_start_str = request.POST.get('data_start')
        data_end_str = request.POST.get('data_end')
        typ_platnosci = request.POST.get('typ_platnosci')
        
        data_od = datetime.strptime(data_start_str, '%Y-%m-%d').date()
        data_do = datetime.strptime(data_end_str, '%Y-%m-%d').date()
        
        if data_do < data_od:
            messages.error(
                request, 
                "Błąd: Data zakończenia urlopu nie może być wcześniejsza niż data jego rozpoczęcia!"
            )
            return render(request, 'urlopomat/urlopomat.html', {'pracownik': pracownik})
        
        dni_urlopu = (data_do - data_od).days + 1
        czy_platny_bool = (typ_platnosci == 'platny')
        
        if czy_platny_bool and dni_urlopu > pracownik.dostepne_dni:
            messages.error(
                request, 
                f"Nie masz wystarczającej liczby dni! Wnioskujesz o {dni_urlopu} dni, a pozostało Ci tylko {pracownik.dostepne_dni}."
            )
            return render(request, 'urlopomat/urlopomat.html', {'pracownik': pracownik})
        
        Wnioski.objects.create(
            skladajacy=pracownik,
            data_od=data_od,
            data_do=data_do,
            czy_platny=czy_platny_bool,
            status="oczekujacy"
        )
        messages.success(request, "Wniosek został pomyślnie wysłany.")
        return redirect('wnioski_page')

    return render(request, 'urlopomat/urlopomat.html', {'pracownik': pracownik})
# ==========================================================================
# Funkcja: wnioski_view
# Przyjmuje: request (HttpRequest) - obiekt żądania przeglądarki
# Co robi: Obsługuje podgląd oraz modyfikację statusów wniosków. Weryfikuje sesję.
#          1. Jeśli żądanie to POST, a użytkownik jest adminem, zmienia status
#             wniosku. Jeśli zaakceptowany wniosek był płatny, pomniejsza pulę dni.
#             Generuje odpowiednie komunikaty powodzenia (messages.success).
#          2. Przy żądaniu GET pobiera zestaw danych filtrowany po uprawnieniach.
# Zwraca: HttpResponse - przekierowanie odświeżające stronę ('wnioski_page') po
#         modyfikacji lub wyrenderowany widok szablonu listy z kontekstem danych.
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
            if wniosek.czy_platny:
                dni = (wniosek.data_do - wniosek.data_od).days + 1
                wniosek.skladajacy.dostepne_dni -= dni
                wniosek.skladajacy.save()
                messages.success(request, f"Zaakceptowano płatny wniosek #{wniosek.id}. Odliczono dni: {dni}.")
            else:
                messages.success(request, f"Zaakceptowano bezpłatny wniosek #{wniosek.id}. Pula dni pracownika nie została zmieniona.")
        elif akcja == 'odrzuc':
            wniosek.status = 'odrzucony'
            messages.success(request, f"Wniosek #{wniosek.id} został odrzucony.")
            
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

def panel_admina_view(request):
    pracownik_id = request.session.get('pracownik_id')
    if not pracownik_id:
        return redirect('login')

    pracownik = Pracownik.objects.get(id=pracownik_id)
    
    if not pracownik.czy_admin:
        return redirect('urlopomat')

    if request.method == 'POST' and 'dodaj_pracownika' in request.POST:
        imie = request.POST.get('imie').strip()
        nazwisko = request.POST.get('nazwisko').strip()
        dostepne_dni = int(request.POST.get('dostepne_dni', 26))
        czy_admin_input = request.POST.get('czy_admin') == 'on'

        if imie and nazwisko:
            generowany_login = f"{imie[0].lower()}{nazwisko.lower()}".replace(" ", "")
            
            licznik = 1
            propozycja_loginu = generowany_login
            while Pracownik.objects.filter(login=propozycja_loginu).exists():
                propozycja_loginu = f"{generowany_login}{licznik}"
                licznik += 1
            generowany_login = propozycja_loginu
            losowe_cyfry = "".join([str(random.randint(0, 9)) for _ in range(3)])
            generowane_haslo = f"{imie}{losowe_cyfry}"
            nowy_pracownik = Pracownik(
                imie=imie,
                nazwisko=nazwisko,
                login=generowany_login,
                dostepne_dni=dostepne_dni,
                czy_admin=czy_admin_input,
                czy_aktywny=True 
            )
            nowy_pracownik.ustaw_haslo(generowane_haslo)
            nowy_pracownik.save()

            messages.success(
                request, 
                f"Pomyślnie dodano pracownika! Login: {generowany_login} | Wygenerowane hasło: {generowane_haslo}"
            )
            return redirect('panel_admina')
    pracownicy_lista = Pracownik.objects.annotate(liczba_wnioskow=Count('zlozone_wnioski'))

    context = {
        'pracownik': pracownik,
        'pracownicy_lista': pracownicy_lista
    }
    return render(request, 'panel/panel.html', context)