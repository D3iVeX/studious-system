from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404:{"message": "No encontrado"}})


products_list = ["Product 1","Product 2","Product 3","Product 4","Product 5"]


@router.get("/")
async def product():
    return ["Product 1","Product 2","Product 3","Product 4","Product 5"]


@router.get("/{id}")
async def products(id: int):
    return products_list[id]
