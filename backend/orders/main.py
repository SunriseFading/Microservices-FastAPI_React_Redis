import time
import requests
import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request


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


class Order(HashModel):
    product_pk: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get_order(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create_order(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()
    request = requests.get(f"{settings.BACKEND_URL}/products/{body['pk']}")
    product = request.json()
    order = Order(
        product_pk=body['pk'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed, order)
    return order


def order_completed(order: Order):
    time.sleep(30)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
