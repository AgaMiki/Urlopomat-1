from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Pracownik(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    login = models.CharField(max_length=50, unique=True)
    haslo = models.CharField(max_length=128)
    dostepne_dni = models.IntegerField(default=26)
    pula_roczna = models.IntegerField(default=26)
    czy_admin = models.BooleanField(default=False)
    czy_aktywny = models.BooleanField(default=True)

    # ==========================================================================
    # Funkcja: ustaw_haslo
    # Przyjmuje: surowe_haslo (str) - hasło w formie czystego tekstu, wpisane przez użytkownika
    # Co robi: Szyfruje (hashuje) surowe hasło za pomocą bezpiecznego algorytmu Django
    #          i zapisuje wynik w polu 'haslo' modelu Pracownik.
    # Zwraca: None
    # ==========================================================================
    def ustaw_haslo(self, surowe_haslo):
        self.haslo = make_password(surowe_haslo)

    # ==========================================================================
    # Funkcja: sprawdz_haslo
    # Przyjmuje: surowe_haslo (str) - hasło wpisane w formularzu podczas logowania
    # Co robi: Porównuje surowe hasło z bezpiecznym, zaszyfrowanym skrótem zapisanym
    #          w bazie danych.
    # Zwraca: bool - True jeśli hasła są zgodne, False w przeciwnym wypadku.
    # ==========================================================================
    def sprawdz_haslo(self, surowe_haslo):
        return check_password(surowe_haslo, self.haslo)

    # ==========================================================================
    # Funkcja: __str__
    # Przyjmuje: self - instancja obiektu Pracownik
    # Co robi: Definiuje tekstową reprezentację obiektu pracownika, przydatną w panelu
    #          oraz podczas debugowania. Uwzględnia status konta.
    # Zwraca: str - ciąg tekstowy zwierający imię, nazwisko i opcjonalną informację o blokadzie.
    # ==========================================================================
    def __str__(self):
        status = "" if self.czy_aktywny else " (nieaktywny)"
        return f"{self.imie} {self.nazwisko}{status}"


class Wnioski(models.Model):
    STATUSY = [
        ('oczekujacy', 'Oczekujący'),
        ('zaakceptowany', 'Zaakceptowany'),
        ('odrzucony', 'Odrzucony'),
    ]
    skladajacy = models.ForeignKey(
        Pracownik,
        on_delete=models.PROTECT,
        related_name='zlozone_wnioski',
    )
    rozpatrujacy = models.ForeignKey(
        Pracownik,
        on_delete=models.PROTECT,
        related_name='rozpatrzone_wnioski',
        null=True,
        blank=True,
    )
    data_od = models.DateField()
    data_do = models.DateField()
    czy_platny = models.BooleanField(default=True)
    opis = models.TextField(blank=True)
    data_zlozenia = models.DateTimeField(auto_now_add=True)
    data_rozpatrzenia = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSY, default='oczekujacy')

    # ==========================================================================
    # Funkcja: __str__
    # Przyjmuje: self - instancja obiektu Wnioski
    # Co robi: Tworzy czytelny opis konkretnego wniosku urlopowego na potrzeby tabel
    #          oraz powiązań w bazie danych.
    # Zwraca: str - ciąg tekstowy zawierający dane składającego oraz zakres dat urlopu.
    # ==========================================================================
    def __str__(self):
        return f"{self.skladajacy} ({self.data_od} - {self.data_do})"