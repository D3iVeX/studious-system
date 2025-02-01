from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, user_schema_db
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})


# Lista de usuarios
users_list = []


@router.get("/", response_model= list[User])
async def users():
    return user_schema_db(db_client.users.find())


@router.get("/{id}") #Path
async def user(id: str): 
    return search_user("_id", ObjectId(id))

@router.get("/search/") #Query
async def user(id: str): 
    return search_user("_id", ObjectId(id))

@router.post("/",response_model= User, status_code = status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        # raise se utiliza para lanzar una excepción en lugar de return. Lanza la excepción HTTPException con el código de estado 404 y el mensaje "User already exists"
        raise HTTPException(status_code=404, detail="User already exists")  

    user_dict = dict(user) 
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model= User)
async def user(user: User):
    
    user_dict = dict(user) 
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}    
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):    
    try:
        db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        return {"message": "Usuario eliminado"}
    except:
        return {"error": "No se ha eliminado el usuario"}       

def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)    
    except:
        return {"error": "El usuario no existe"}
