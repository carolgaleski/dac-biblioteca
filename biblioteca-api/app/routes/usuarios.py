from fastapi import APIRouter, HTTPException
from app.models import Usuario
from app.db import usuarios_db

router = APIRouter()

usuarios_db = []

def usuario_to_hateoas(usuario):
    links = [
        {"rel": "self", "href": f"/usuarios/{usuario.id}", "method": "GET"},
        {"rel": "update", "href": f"/usuarios/{usuario.id}", "method": "PUT"},
        {"rel": "delete", "href": f"/usuarios/{usuario.id}", "method": "DELETE"},
    ]
    return {**usuario.dict(), "_links": links}

@router.get("/")
def listar_usuarios():
    return [usuario_to_hateoas(u) for u in usuarios_db]



@router.get("/{usuario_id}")
def buscar_usuario(usuario_id: int):
    usuario = next((u for u in usuarios_db if u.id == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_to_hateoas(usuario)



@router.post("/")
def criar_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return usuario_to_hateoas(usuario)



@router.put("/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario_atualizado: Usuario):
    for i, usuario in enumerate(usuarios_db):
        if usuario.id == usuario_id:
            usuarios_db[i] = usuario_atualizado
            return usuario_to_hateoas(usuario_atualizado)
    raise HTTPException(status_code=404, detail="Usuário não encontrado")



@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int):
    for i, usuario in enumerate(usuarios_db):
        if usuario.id == usuario_id:
            return usuarios_db.pop(i)
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
