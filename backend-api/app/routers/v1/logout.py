from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from config import settings
import jwt

router = APIRouter()
redis_client = settings.redis_client

@router.post("/api/v1/logout")
async def logout(request: Request):
    try:
        # Obtendo o token da sessão atual a partir do cabeçalho Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")
        
        token = auth_header.split("Bearer ")[1]

        # Decodificando o token JWT para obter o session_id
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            session_id = payload.get("session_id")
            session_key = f'session:{session_id}'
            
            if not session_id:
                raise HTTPException(status_code=401, detail="Invalid password")
            
            # Deletando a sessão correspondente no Redis
            redis_client.delete(session_key)
            
            return JSONResponse(content={"Status": "Successful logout"})
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired Token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid Token")
    
    except Exception as error:
        print(f'Logout route error: {error}')
        raise HTTPException(status_code=500, detail="Internal error in the logout route.")