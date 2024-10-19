from fastapi import FastAPI, Request, HTTPException
from routers.v1 import isalive, login, logout, register, categories, data
from config import settings
import jwt
import uvicorn

app = FastAPI()
redis_client = settings.redis_client

# Middleware de verificação de sessão
EXCLUDED_PATHS = ["/api/v1/isalive", "/api/v1/login", "/api/v1/register"] # Rotas ignoradas pelo middleware

# Função que verifica a se o token e a sessão do usuário é válida.
async def verify_session_middleware(request: Request, call_next):
    if request.url.path.startswith("/api") and request.url.path not in EXCLUDED_PATHS:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        token = auth_header.split("Bearer ")[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            session_id = payload.get("session_id")
            session_key = f'session:{session_id}'
            
            if not session_id or not redis_client.exists(session_key):
                raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        except jwt.ExpiredSignatureError:
            if session_id:
                redis_client.delete(f'session:{session_id}')
            raise HTTPException(status_code=401, detail="Token expired: Your session was removed.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    response = await call_next(request)
    return response

# Adiciona o middleware na aplicação
app.middleware('http')(verify_session_middleware)

# Incluindo as Rotas
app.include_router(isalive.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(categories.router)
app.include_router(data.router)

@app.get('/')
def inicializacao() -> str:
    return 'API em execução...'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
