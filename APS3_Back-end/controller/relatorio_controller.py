from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from service import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/eventos/ocupacao")
def consultar_ocupacao(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_ocupacao(db)

@router.get("/eventos/categorias")
def consultar_categorias(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_categorias(db)

@router.get("/participantes/cursos")
def consultar_cursos(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_cursos(db)
