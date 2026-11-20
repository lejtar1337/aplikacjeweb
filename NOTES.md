# Stan początkowy laboratorium 5

Katalog jest kopią `labs/04-api-contract/solution/` bez zmian: cały backend w `app/main.py`, frontend z modułami `api.js`, `ui.js`, `main.js` oraz skrypt `check-api.sh`.

## Kto czego potrzebuje

| Sytuacja | Co zrobić |
|---|---|
| własny projekt po laboratorium 4, z zadaniami samodzielnymi | nic, kontynuujesz własny projekt |
| własny projekt bez zadania samodzielnego 4 | skopiuj `check-api.sh` z tego katalogu |
| własny projekt bez zadań 1 i 2 | nic, `check-api.sh` pokaże kilka niezgodności, liczy się ten sam wynik przed i po refaktoryzacji |
| brak projektu | skopiuj cały katalog |

## Uruchomienie

Terminal 1:

```bash
uv sync
uv run fastapi dev app/main.py
```

Terminal 2:

```bash
uv run python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Terminal 3:

```bash
./check-api.sh
```

Przeglądarka: `http://127.0.0.1:5500`, API: `http://127.0.0.1:8000/docs`.
