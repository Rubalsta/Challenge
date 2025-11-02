from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers
from app.routers import auth, users, posts,comments,tags

# importar middleware 
from app.middleware.logging import ResponseTimeMiddleware

app = FastAPI(
    title="Blog Random",
    description="Blog Random para el Challenge (API)",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agrega middleware de logging de tiempo de respuesta
app.add_middleware(ResponseTimeMiddleware)

#Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(tags.router)

@app.get("/")
async def root():
    """abre documentacion directamente para mayor accesibilidad"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")
