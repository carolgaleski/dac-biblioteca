from fastapi import APIRouter, HTTPException
from datetime import date
from app.db import livros_db, emprestimos_db

router = APIRouter()

emprestimos_db = []

class Emprestimo:
    def __init__(self, id: int, livro_id: int, usuario_id: int, data_emprestimo: str, devolvido: bool = False):
        self.id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.data_emprestimo = data_emprestimo
        self.devolvido = devolvido

def emprestimo_to_hateoas(e):
    links = [{"rel": "self", "href": f"/emprestimos/{e.id}", "method": "GET"}]
    if not e.devolvido:
        links.append({"rel": "devolver", "href": f"/emprestimos/{e.id}/devolucao", "method": "PUT"})
    return {**e.__dict__, "_links": links}



@router.get("/")
def listar_emprestimos():
    return [emprestimo_to_hateoas(e) for e in emprestimos_db]



@router.post("/")
def criar_emprestimo(id: int, livro_id: int, usuario_id: int):
    livro = next((l for l in livros_db if l.id == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if not livro.disponivel:
        raise HTTPException(status_code=409, detail="Livro já está emprestado")
    novo = Emprestimo(id=id, livro_id=livro_id, usuario_id=usuario_id, data_emprestimo=str(date.today()))
    emprestimos_db.append(novo)
    livro.disponivel = False
    return emprestimo_to_hateoas(novo)



@router.put("/{emprestimo_id}/devolucao")
def devolver_emprestimo(emprestimo_id: int):
    emprestimo = next((e for e in emprestimos_db if e.id == emprestimo_id), None)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    if emprestimo.devolvido:
        raise HTTPException(status_code=409, detail="Livro já devolvido")
    emprestimo.devolvido = True
    livro = next((l for l in livros_db if l.id == emprestimo.livro_id), None)
    if livro:
        livro.disponivel = True
    return emprestimo_to_hateoas(emprestimo)
