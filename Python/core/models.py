from django.db import models

# Create your models here.
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

    def ustaw_haslo(self, surowe_haslo):
        self.haslo = make_password(surowe_haslo)

    def sprawdz_haslo(self, surowe_haslo):
        return check_password(surowe_haslo, self.haslo)

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

    def __str__(self):
        return f"{self.skladajacy} ({self.data_od} - {self.data_do})"