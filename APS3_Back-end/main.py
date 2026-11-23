from fastapi import FastAPI
from database import Base, engine
from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router
from controller.relatorio_controller import router as relatorio_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento persistente de eventos acadêmicos, participantes, inscrições e relatórios.",
    version="2.0.0"
)
app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(relatorio_router)

@app.get("/")
def inicio():
    return {"mensagem": "API de Eventos Acadêmicos funcionando com SQLite!",
            "documentacao": "/docs"}
