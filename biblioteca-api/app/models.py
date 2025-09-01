from pydantic import BaseModel
from typing import Optional

#nota: basemodel é usado para validar e serializadr dados em json

class Autor(BaseModel):
    id: int 
    nome: str

class Livro(BaseModel):
    id: int
    titulo: str
    ano_publicacao: int
    disponivel: bool
    autor: Autor

class Usuario(BaseModel):
    id: int
    nome: str 
    email: str