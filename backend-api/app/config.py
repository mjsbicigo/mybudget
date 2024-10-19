from os import environ
from redis import Redis

# Definindo as variáveis de ambiente:
    # URI de conexão com o MongoDB  
    # URI de Conexão com o Redis
    # Secret Key usada para assinar transações
    
class Settings:
    MONGO_URI = environ.get("MONGO_URI")
    REDIS_URI = environ.get("REDIS_URI")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    # Inicia conexão com o Redis
    redis_client = Redis.from_url(REDIS_URI)
    try:
        # Tenta realizar uma operação básica no Redis
        redis_client.ping()
        print("Connected to Redis!")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        raise e
    
    # Verificando se as variáveis de ambiente existem
    def __init__(self):
        if not self.MONGO_URI:
            raise ValueError("Missing environment variable: MONGO_URI")
        if not self.REDIS_URI:
            raise ValueError("Missing environment variable: REDIS_URI")
        if not self.SECRET_KEY:
            raise ValueError("Missing environment variable: SECRET_KEY")

settings = Settings()
