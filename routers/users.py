from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

# Entidad users
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Lista de usuarios
users_list = [User(id=1,name="David",surname="D3iveX",url="https:1",age=25),
              User(id=2,name="John",surname="Doe",url="https:2",age=30),
              User(id=3,name="Jane",surname="Doe",url="https:3",age=28)]


# Rutas de la API para obtener usuarios
@router.get("/users2")
async def usersjson():
    return [{"name": "David","surname": "D3iveX","url":"https:1", "age": 25},
            {"name": "John","surname": "Doe","url":"https:2", "age": 30},
            {"name": "Jane","surname": "Doe","url":"https:3", "age": 28}]

# Rutas de la API para obtener usuarios con la entidad User
@router.get("/users")
async def users():
    return users_list

# Por path. Se suele utilizar para obtener un recurso en concreto. Ejemplo: /user/1, /user/2, /user/3 es decir, cuando tenemos un parametro fijo
# Ejemplo --> búsqueda de un usuario por nombre, búsqueda de un usuario por apellido, etc.
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Por query Ejemplo: /?id=1, /?id=2, /?id=3. Se utiliza query para los parámetros que no son fijos y no van a ser necesarios para realizar la consulta
# Ejemplo --> Busqueda en una bbdd con paginación (publicación de la 1 a la 10)

@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

def search_user(id: int):
    filtered_users = filter(lambda user: user.id == id, users_list)
    try:
        return list(filtered_users)[0]
    except IndexError:
        return {"error": "El usuario ya existe"}


@router.post("/user/",response_model= User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        # raise se utiliza para lanzar una excepción en lugar de return. Lanza la excepción HTTPException con el código de estado 404 y el mensaje "User already exists"
        raise HTTPException(status_code=404, detail="User already exists")        
    else:
        users_list.append(user)
        return user


@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True            
            break        
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            break
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return {"message": "Usuario eliminado"}
