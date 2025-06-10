# Django Transaction Journal
**System zarządzania osobistymi transakcjami finansowymi**

## Spis treści
- [Opis projektu](#opis-projektu)
- [Funkcjonalności](#funkcjonalności)
- [Wymagania systemowe](#wymagania-systemowe)
- [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
- [Korzystanie z Dockera](#korzystanie-z-dockera)
- [Struktura projektu](#struktura-projektu)
- [Testy](#testy)
- [API kursów walut](#api-kursów-walut)

## Opis projektu
Django Transaction Journal to aplikacja webowa do zarządzania osobistymi finansami, umożliwiająca śledzenie dochodów i wydatków z zaawansowanym systemem kategoryzacji i raportowania.

## Funkcjonalności

###  System użytkowników
- Rejestracja nowych użytkowników
- Logowanie i wylogowywanie
- Resetowanie hasła (z powiadomieniem email)
- Izolacja danych między użytkownikami

###  Zarządzanie transakcjami
- Dodawanie nowych transakcji (dochody/wydatki)
- Edycja istniejących transakcji
- Usuwanie transakcji
- Lista transakcji z paginacją (50 na stronę)
- Filtrowanie transakcji według:
  - Typu (dochód/wydatek)
  - Kategorii
  - Zakresu dat
- Numeracja transakcji od najnowszych

###  System kategorii
- Predefiniowane kategorie bazowe (Other, Clothing & Footwear, Education, Income, Utilities, Travel, Entertainment, Health, Transportation, Groceries)
- Tworzenie własnych kategorii użytkownika
- Edycja i usuwanie kategorii użytkownika
- Walidacja nazw kategorii (unikalne dla użytkownika)
- Automatyczne generowanie slug dla kategorii

###  Statystyki i raporty
- Podsumowanie ogólne (łączne dochody, wydatki, saldo)
- Statystyki według kategorii
- Obliczanie salda dla każdej kategorii

###  Kursy walut
- Aktualne kursy walut z API CurrencyFreaks
- Obsługa 11 walut: USD, EUR, GBP, JPY, RUB, CNY, CHF, UAH, PLN, CAD, AUD
- Cache na 1 godzinę dla lepszej wydajności
- Wyświetlanie symboli walut i flag krajów

### Bezpieczeństwo i walidacja
- Kontrola dostępu - użytkownicy widzą tylko swoje dane
- Walidacja kwot transakcji (nie mogą być ujemne)
- Ochrona przed edycją kategorii bazowych
- Obsługa błędów 403, 404, 500 z custom szablonami

### Wymagania systemowe
- Python 3.8+
- Django 5.2.1
- SQLite (domyślnie) lub PostgreSQL
- Połączenie internetowe (dla API kursów walut)

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium
```bash
git clone <url-repozytorium>
cd djangotestproject
```

### 2. Utwórz wirtualne środowisko
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 4. Wykonaj migracje bazy danych
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Utwórz superusera (opcjonalnie)
```bash
python manage.py createsuperuser
```

### 6. Uruchom serwer deweloperski
```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:8000/`

## Korzystanie z Dockera

### Uruchomienie z Docker Compose
```bash
docker-compose up --build
```

### Dostęp do kontenera
```bash
docker-compose exec web bash
```

### Zatrzymanie
```bash
docker-compose down
```

## Struktura projektu

### Aplikacje
- **testsite/** - główna aplikacja z logiką transakcji i kategorii
- **users/** - obsługa systemu użytkowników
- **djangotestproject/** - konfiguracja główna projektu

### Template'y
- Responssywne szablony HTML z Bootstrap
- Obsługa błędów (403, 404, 500)
- Modularna struktura z include'ami

### Statyczne pliki
- Custom CSS (`testsite/static/testsite/css/styles.css`)
- Responsive design

## Testy
Projekt zawiera kompleksowe testy jednostkowe:

```bash
# Uruchomienie wszystkich testów
python manage.py test

# Testy konkretnej aplikacji
python manage.py test testsite
python manage.py test users

# Testy z większą szczegółowością
python manage.py test --verbosity=2
```

### Pokrycie testami:
- **Models**: walidacja danych, constraints, metody
- **Views**: funkcjonalność widoków, permissions
- **URLs**: routing i nazwy URL

## API kursów walut
Aplikacja korzysta z [CurrencyFreaks API](https://currencyfreaks.com/) do pobierania aktualnych kursów walut.

### Obsługiwane waluty:
| Kod | Waluta | Symbol | Flaga |
|-----|--------|--------|-------|
| USD | Dolar amerykański | $ | 🇺🇸 |
| EUR | Euro | € | 🇪🇺 |
| GBP | Funt brytyjski | £ | 🇬🇧 |
| JPY | Jen japoński | ¥ | 🇯🇵 |
| RUB | Rubel rosyjski | ₽ | 🇷🇺 |
| CNY | Yuan chiński | ¥ | 🇨🇳 |
| CHF | Frank szwajcarski | kr | 🇨🇭 |
| UAH | Hrywna ukraińska | ₴ | 🇺🇦 |
| PLN | Złoty polski | zł | 🇵🇱 |
| CAD | Dolar kanadyjski | C$ | 🇨🇦 |
| AUD | Dolar australijski | A$ | 🇦🇺 |

## Zależności (requirements.txt)
```
asgiref==3.8.1
certifi==2025.4.26
charset-normalizer==3.4.2
Django==5.2.1
django-debug-toolbar==5.2.0
django-extensions==4.1
idna==3.10
requests==2.32.3
sqlparse==0.5.3
urllib3==2.4.0
```



