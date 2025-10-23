from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import students , users
from src.routers.auth import auth



app = FastAPI(title="Sistema de registro de catequesisis",
              description="API para gestionar el registro de catequesis",
               version="1.0.0")


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

@app.get("/")
def read_root():
  return {"message": "Bienvenido al sistema de registro de catequesis"}
