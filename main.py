from fastapi import FastAPI
from routers import users, products, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(users.router)
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hello Fast API"

@app.get("/url")
async def url():
    return {"message": "Hello World"}



