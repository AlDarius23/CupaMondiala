import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

NUME_DB = "batrani.db"

aplicatie = FastAPI(title="Batranii fara Cupa Mondiala")


class Batran(BaseModel):
    id: int
    nume: str
    varsta: int
    tara: str
    post: str


def conectare():
    conexiune = sqlite3.connect(NUME_DB)
    conexiune.row_factory = sqlite3.Row
    return conexiune


@aplicatie.get("/")
def acasa():
    return {"mesaj": "Mergi pe /batrani sau pe /docs"}


@aplicatie.get("/batrani", response_model=list[Batran])
def toti_batranii(tara: str = None):
    conexiune = conectare()
    if tara is None:
        cursor = conexiune.execute("SELECT * FROM batrani ORDER BY varsta DESC")
    else:
        cursor = conexiune.execute(
            "SELECT * FROM batrani WHERE tara = ? ORDER BY varsta DESC",
            (tara,)
        )
    randuri = cursor.fetchall()
    conexiune.close()
    batrani = []
    for rand in randuri:
        batrani.append(Batran(**dict(rand)))
    return batrani


@aplicatie.get("/batrani/{id_batran}", response_model=Batran)
def un_batran(id_batran: int):
    conexiune = conectare()
    cursor = conexiune.execute("SELECT * FROM batrani WHERE id = ?", (id_batran,))
    rand = cursor.fetchone()
    conexiune.close()
    if rand is None:
        raise HTTPException(status_code=404, detail="Nu exista jucatorul asta")
    return Batran(**dict(rand))
