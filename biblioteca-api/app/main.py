from fastapi import FastAPI
from app.routes.livros import router as livros_router
from app.routes.autores import router as autores_router
from  app.routes.emprestimos import router as emprestimos_router
from app.routes.usuarios import router as usuarios_router

app = FastAPI(title="API Biblioteca")

app.include_router(livros_router, prefix="/livro")
app.include_router(autores_router, prefix="/autor")
app.include_router(emprestimos_router, prefix="/emprestimos")
app.include_router(usuarios_router, prefix="/usuarios")


