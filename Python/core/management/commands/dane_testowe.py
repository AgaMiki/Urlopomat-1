from django.core.management.base import BaseCommand
from core.models import Pracownik, Wnioski
from datetime import date, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Tworzy przykładowych pracowników i wnioski urlopowe"

    def handle(self, *args, **options):
        # czyścimy stare dane, żeby nie dublować przy ponownym odpaleniu
        Wnioski.objects.all().delete()
        Pracownik.objects.all().delete()

        # --- pracownicy ---
        admin = Pracownik(imie="Agata", nazwisko="Kowalska", login="akowalska", czy_admin=True)
        admin.ustaw_haslo("admin123")
        admin.save()

        anna = Pracownik(imie="Anna", nazwisko="Nowak", login="anowak", dostepne_dni=18)
        anna.ustaw_haslo("anna123")
        anna.save()

        piotr = Pracownik(imie="Piotr", nazwisko="Wiśniewski", login="pwisniewski", dostepne_dni=26)
        piotr.ustaw_haslo("piotr123")
        piotr.save()

        nieaktywny = Pracownik(imie="Jan", nazwisko="Były", login="jbyly", czy_aktywny=False)
        nieaktywny.ustaw_haslo("jan123")
        nieaktywny.save()

        # --- wnioski ---
        # zaakceptowany, rozpatrzony przez admina
        Wnioski.objects.create(
            skladajacy=anna,
            rozpatrujacy=admin,
            data_od=date(2026, 7, 1),
            data_do=date(2026, 7, 14),
            czy_platny=True,
            opis="Urlop letni",
            data_rozpatrzenia=timezone.now(),
            status="zaakceptowany",
        )

        # oczekujący, jeszcze nikt nie rozpatrzył
        Wnioski.objects.create(
            skladajacy=piotr,
            data_od=date(2026, 8, 10),
            data_do=date(2026, 8, 12),
            czy_platny=True,
            opis="Sprawy rodzinne",
            status="oczekujacy",
        )

        # odrzucony
        Wnioski.objects.create(
            skladajacy=anna,
            rozpatrujacy=admin,
            data_od=date(2026, 12, 24),
            data_do=date(2026, 12, 31),
            czy_platny=False,
            opis="Urlop świąteczny bezpłatny",
            data_rozpatrzenia=timezone.now(),
            status="odrzucony",
        )

        self.stdout.write(self.style.SUCCESS(
            f"Gotowe: {Pracownik.objects.count()} pracowników, "
            f"{Wnioski.objects.count()} wniosków."
        ))