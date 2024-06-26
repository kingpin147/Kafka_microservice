from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")
    
except FileNotFoundError:
    config = Config()
    
DATABASE_URL: str = config("DATABASE_URL", cast=Secret)
TestTable_URL:str = config("TestTable_URL", cast=Secret)
BOOTSTRAP_SERVER: str = config("BOOTSTRAP_SERVER", cast=Secret)
KAFKA_ORDER_TOPIC: str = config("KAFKA_ORDER_TOPIC", cast=Secret)
KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT: str = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast=Secret)

