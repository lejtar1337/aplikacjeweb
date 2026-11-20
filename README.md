# TaskBoard

System zarzadzania projektami i zadaniami rozwijany na laboratoriach przedmiotu
Podstawy programowania aplikacji webowych.

## Uruchomienie

API:

```bash
uv sync
uv run fastapi dev app/main.py
```

Frontend, w drugim terminalu:

```bash
uv run python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

API: http://127.0.0.1:8000, frontend: http://127.0.0.1:5500

Frontend musi byc otwierany pod adresem `http://127.0.0.1:5500`. Ten origin jest
wpisany w konfiguracji CORS. Adres `http://localhost:5500` jest innym origin.

Kontrola kontraktu, przy uruchomionym API:

```bash
./check-api.sh
```

## Zasoby

| Metoda | Sciezka | Sukces | Bledy |
|---|---|---|---|
| GET | `/projects` | 200 | |
| POST | `/projects` | 201 | 409, 422 |
| GET | `/projects/{project_id}` | 200 | 404 |
| PATCH | `/projects/{project_id}` | 200 | 404, 409, 422 |
| DELETE | `/projects/{project_id}` | 204 | 404, 409 |
| GET | `/users` | 200 | |
| GET | `/users/{user_id}` | 200 | 404 |
| GET | `/tasks` | 200 | 422 |
| POST | `/tasks` | 201 | 400, 409, 422 |
| GET | `/tasks/{task_id}` | 200 | 404 |
| PATCH | `/tasks/{task_id}` | 200 | 400, 404, 409, 422 |
| DELETE | `/tasks/{task_id}` | 204 | 404 |

Parametry `GET /tasks`: `status`, `project_id`, `assignee_id`, `limit` (1-100, domyslnie 20).

Pomocnicze: `GET /`, `GET /health`, dokumentacja `GET /docs`.

### Decyzje projektowe

- Zadanie nalezy do projektu. Relacje wyraza filtr `GET /tasks?project_id=1`, a nie zagniezdzenie `/projects/1/tasks`.
- Zadanie zmieniamy przez PATCH. PUT zostal usuniety.
- Uzytkownicy sa tylko do odczytu. Tworzenie kont wymaga rejestracji (zajecia 8).
- Tytul zadania jest unikalny w obrebie projektu.
- Projektu z zadaniami nie mozna usunac (409).
- Odwolanie w ciele zadania do nieistniejacego projektu lub uzytkownika to 422, a nie 404.
- Wszystkie bledy maja format Problem Details (RFC 9457).

## Frontend

| Plik | Odpowiedzialnosc |
|---|---|
| `frontend/js/api.js` | komunikacja z API |
| `frontend/js/ui.js` | operacje na DOM |
| `frontend/js/main.js` | obsluga zdarzen, polaczenie obu modulow |

## Stan projektu

Po laboratorium 4: API z zasobami projektow, uzytkownikow i zadan, osobnymi
modelami wejscia i wyjscia, walidacja oraz jednolitym formatem bledow.
Frontend pokazuje zadania projektu 1.

Dane sa przechowywane w pamieci procesu i znikaja po restarcie serwera.
Trwalosc danych zostanie dodana na zajeciach 6.
