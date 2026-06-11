# ETL cu Python, SQLite si FastAPI

Pipeline care extrage jucatori de fotbal printr-un request HTTP, pastreaza
doar legendele de peste 34 de ani fara Cupa Mondiala, ii salveaza in SQLite
si ii expune printr-un API de FastAPI.

## Fisiere

- `date/jucatori.json` - lista cu 30 de jucatori (datele sursa)
- `server_date.py` - un server mic care serveste JSON-ul prin HTTP, ca sa am de unde sa fac request real cu requests
- `etl.py` - extrage, filtreaza si salveaza in `batrani.db`
- `api.py` - API-ul de FastAPI care citeste din baza de date

## Cum se ruleaza

```
pip install -r requirements.txt
```

Apoi, in primul terminal:

```
python server_date.py
```

In al doilea terminal:

```
python etl.py
uvicorn api:aplicatie --reload
```

Dupa aia intri pe http://127.0.0.1:8000/docs si te joci cu API-ul.

Rute disponibile:
- `/batrani` - toti, sortati dupa varsta
- `/batrani?tara=Uruguay` - filtrare dupa tara
- `/batrani/3` - un singur jucator dupa id

## Testare

Asa arata cand rulez ETL-ul:

```
$ python etl.py
Iau jucatorii de pe net...
Am primit 30 jucatori
Au ramas 15 batrani fara Cupa Mondiala
Gata, i-am salvat in batrani.db
```

Si asa porneste serverul:

```
$ uvicorn api:aplicatie --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [4821] using StatReload
INFO:     Started server process [4823]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Cateva request-uri de test:

```
$ curl "http://127.0.0.1:8000/batrani?tara=Uruguay"
[{"id":6,"nume":"Edinson Cavani","varsta":39,"tara":"Uruguay","post":"atacant"},
 {"id":7,"nume":"Luis Suarez","varsta":39,"tara":"Uruguay","post":"atacant"}]

$ curl http://127.0.0.1:8000/batrani/99
{"detail":"Nu exista jucatorul asta"}
```

```
INFO:     127.0.0.1:41612 - "GET /batrani HTTP/1.1" 200 OK
INFO:     127.0.0.1:41620 - "GET /batrani?tara=Uruguay HTTP/1.1" 200 OK
INFO:     127.0.0.1:41622 - "GET /batrani/99 HTTP/1.1" 404 Not Found
```

## De ce server mock

Nu am gasit un API public gratuit care sa zica si varsta si daca jucatorul a castigat mondialul, asa ca mi-am facut eu datele si le servesc local prin HTTP. Request-ul din `etl.py` e unul real, deci daca gasesc vreodata un API bun, schimb doar `URL_DATE` si merge la fel.
