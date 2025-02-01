from pydantic import BaseModel


# Entidad users
class User(BaseModel):
    id: str | None = None
    username: str
    email: str