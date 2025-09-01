from fastapi import APIRouter, HTTPException
from app.models import Autor

router = APIRouter()

autores_db = []

@router.post("/")
def criar_autor(autor: Autor):
    autores_db.append(autor)
    return autor


@router.get("/")
def listar_autores():
    return autores_db


def buscar_autor(autor_id: int):
    for autor in autores_db:
        if autor.id == autor_id:
            return autor
    raise HTTPException(status_code=404, detail="Autor não encontrado")


@router.put("/{autor_id}")
def atualizar_autor(autor_id: int, autor_atualizado: Autor):
    for i, autor in enumerate(autores_db):
        if autor.id == autor_id:
            autores_db[i] = autor_atualizado
            return autor_atualizado
    raise HTTPException(status_code=404, detail="Autor não encontrado")


@router.delete("/{autor_id}")
def deletar_autor(autor_id: int):
    for i, autor in enumerate(autores_db):
        if autor.id == autor_id:
            return autores_db.pop(i)
    raise HTTPException(status_code=404, detail="Autor não encontrado")