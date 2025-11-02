from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
from app.routers import auth, users

app = FastAPI(
    title="Blog Random",
    description="Blog Random para el Challenge (API)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    """Abrir Documentacion"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")
