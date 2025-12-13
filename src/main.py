from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.routers import students , users , catechists, parents
from src.routers.auth import auth



app = FastAPI(title="Sistema de registro de catequesisis",
              description="API para gestionar el registro de catequesis",
               version="1.0.0",
               terms_of_service= "https://catequesis.org/terms/",
               contact={
        "name": "Equipo Catequesis Digital",
        "url": "https://catequesis.org",
        "email": "soporte@catequesis.org",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Oculta modelos al inicio
        "docExpansion": "none",          # Contrae rutas por defecto
        "displayRequestDuration": True,  # Muestra tiempo de respuesta
        "filter": True,                  # Activa barra de búsqueda
        "syntaxHighlight.theme": "monokai",  # Tema oscuro
    },)


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.routerAuth)
app.include_router(students.routerStudents)
app.include_router(users.routerUsers)
app.include_router(catechists.routerCatechists)
app.include_router(parents.routerParents)

# Static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
  return {"message": "Bienvenido al sistema de registro de catequesis"}


