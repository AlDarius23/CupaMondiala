import requests
import sqlite3

URL_DATE = "http://127.0.0.1:8001/jucatori.json"
NUME_DB = "batrani.db"
VARSTA_LIMITA = 34


def ia_toti_jucatorii():
    raspuns = requests.get(URL_DATE, timeout=10)
    raspuns.raise_for_status()
    return raspuns.json()


def filtreaza_batranii(toti_jucatorii):
    batrani = []
    for jucator in toti_jucatorii:
        if jucator["varsta"] > VARSTA_LIMITA:
            if jucator["a_castigat_mondialul"] is False:
                batran = {
                    "nume": jucator["nume"],
                    "varsta": jucator["varsta"],
                    "tara": jucator["tara"],
                    "post": jucator["post"]
                }
                batrani.append(batran)
    return batrani


def salveaza_batranii(batrani):
    conexiune = sqlite3.connect(NUME_DB)
    conexiune.execute("""
        CREATE TABLE IF NOT EXISTS batrani (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT,
            varsta INTEGER,
            tara TEXT,
            post TEXT
        )
    """)
    conexiune.execute("DELETE FROM batrani")
    for batran in batrani:
        conexiune.execute(
            "INSERT INTO batrani (nume, varsta, tara, post) VALUES (?, ?, ?, ?)",
            (batran["nume"], batran["varsta"], batran["tara"], batran["post"])
        )
    conexiune.commit()
    conexiune.close()


if __name__ == "__main__":
    print("Iau jucatorii de pe net...")
    toti_jucatorii = ia_toti_jucatorii()
    print("Am primit " + str(len(toti_jucatorii)) + " jucatori")
    batrani = filtreaza_batranii(toti_jucatorii)
    print("Au ramas " + str(len(batrani)) + " batrani fara Cupa Mondiala")
    salveaza_batranii(batrani)
    print("Gata, i-am salvat in " + NUME_DB)
