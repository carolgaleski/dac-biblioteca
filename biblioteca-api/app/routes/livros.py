from fastapi import APIRouter, HTTPException
from app.models import Livro, Autor
from app.db import livros_db, autores_db, emprestimos_db  


router = APIRouter()

livros_db = []
autores_db = [Autor(id=1, nome="Taylor Jenkins Reid")]

def livro_to_hateoas(livro: Livro):
    links = [
        {"rel": "self", "href": f"/livros/{livro.id}", "method": "GET"},
        {"rel": "update", "href": f"/livros/{livro.id}", "method": "PUT"},
        {"rel": "delete", "href": f"/livros/{livro.id}", "method": "DELETE"},
    ]
    if livro.disponivel:
        links.append({"rel": "emprestar", "href": "/emprestimos", "method": "POST"})
    else:
        emprestimo = next((e for e in emprestimos_db if e['livro_id'] == livro.id and not e['devolvido']), None)
        if emprestimo:
            links.append({"rel": "devolver", "href": f"/emprestimos/{emprestimo['id']}/devolucao", "method": "PUT"})
    return {**livro.dict(), "_links": links}


@router.get("/")
def listar_livros():
    return [livro_to_hateoas(l) for l in livros_db]



@router.get("/{livro_id}")
def buscar_livro(livro_id: int):
    livro = next((l for l in livros_db if l.id == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro_to_hateoas(livro)



@router.post("/")
def criar_livro(livro: Livro):
    livros_db.append(livro)
    return livro_to_hateoas(livro)



@router.put("/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    for i, livro in enumerate(livros_db):
        if livro.id == livro_id:
            livros_db[i] = livro_atualizado
            return livro_to_hateoas(livro_atualizado)
    raise HTTPException(status_code=404, detail="Livro não encontrado")



@router.delete("/{livro_id}")
def deletar_livro(livro_id: int):
    for i, livro in enumerate(livros_db):
        if livro.id == livro_id:
            return livros_db.pop(i)
    raise HTTPException(status_code=404, detail="Livro não encontrado")
