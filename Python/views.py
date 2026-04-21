from django.shortcuts import render

def budget_view(request):
    context = {}
    
    if request.method == 'POST':
        # Pobieranie danych z formularza HTML
        stypendium = float(request.POST.get('stypendium', 0) or 0)
        praca = float(request.POST.get('praca', 0) or 0)
        rodzina = float(request.POST.get('rodzina', 0) or 0)
        
        mieszkanie = float(request.POST.get('mieszkanie', 0) or 0)
        jedzenie = float(request.POST.get('jedzenie', 0) or 0)
        transport = float(request.POST.get('transport', 0) or 0)
        
        # Koszty auta
        auto_check = request.POST.get('auto')
        przebieg = float(request.POST.get('przebieg', 0) or 0)
        styl = request.POST.get('styl')
        
        koszt_auta = 0
        if auto_check == 'tak':
            stawka = 0.65 if styl == 'miasto' else 0.45
            koszt_auta = przebieg * stawka

        # Obliczenia
        suma_dochodow = stypendium + praca + rodzina
        suma_wydatkow = mieszkanie + jedzenie + transport + koszt_auta
        bilans = suma_dochodow - suma_wydatkow
        
        # Określanie statusu i koloru dla Bootstrapa
        if bilans > 0:
            status, kolor = "Nadwyżka", "success"
        elif bilans == 0:
            status, kolor = "Zrównoważony", "info"
        else:
            status, kolor = "Deficyt", "danger"

        context = {
            'dochody': suma_dochodow,
            'wydatki': suma_wydatkow,
            'bilans': bilans,
            'status': status,
            'kolor': kolor,
            'obliczono': True
        }
    
    return render(request, 'budget/index.html', context)
