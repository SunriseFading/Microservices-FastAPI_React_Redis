import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=settings.HOST,
    port=settings.PORT,
    password=settings.PASSWORD,
    decode_responses=True)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def get_all_products():
    return [Product.get(pk) for pk in Product.all_pks()]


@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)


@app.post('/products')
def create_product(product: Product):
    return product.save()


@app.delete('/products/{pk}')
def delete_product(pk: str):
    return Product.delete(pk)
