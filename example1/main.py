from typing import Union
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

lista_alumnos = []

class InputPut(BaseModel):
    id: int = Field(..., gt=-1)
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/alumnos")
def get_alumnos():
    return {"alumnos": ", ".join(lista_alumnos)}

@app.post("/alumno")
def create_alumno(name: str):
    lista_alumnos.append(name)
    return "Se agrego un nuevo alumno"

@app.put("/alumno")
def modify_alumno(id: int, name: str):
    try:
        nombre_original = lista_alumnos[id]
        lista_alumnos[id] = name
        return "Se modificó el nomnbre del alumno " + nombre_original + " por " + name
    except IndexError:
        return "No tenemos un alumno con ese índice"

@app.delete("/alumno")
def delete_alumno(id: int):
    try:
        alumnos_eliminado = lista_alumnos.pop(id)
        return "Se eliminó el alumno " + alumnos_eliminado
    except IndexError:
        return "No tenemos un alumno con ese índice"