from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager, contextmanager
from microservice import settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

# Defining the Order model
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    product_id: int
    product_name: str
    product_price: int

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print('Call Kafka consumer')
    yield

# Start app
app = FastAPI(
    lifespan=lifespan, 
    title="Product Service API With Kafka", 
    version="1.0.0",
    servers=[{"url": "http://127.0.0.1:8000", "description": "Development server"}]
)
# setting root message
@app.get("/")
async def root():
    return {"Test": "Product Service API With Kakfa"}

@app.post("/create_order")
async def create_order(order: Order):
    producer=AIOKafkaProducer(settings.BOOTSTRAP_SERVER) 
    await producer.start()
    productJson=json.dumps(order.__dict__).encode('utf-8')
    try:
        await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC)
        print(productJson)
    finally:
        await producer.stop()
    return productJson