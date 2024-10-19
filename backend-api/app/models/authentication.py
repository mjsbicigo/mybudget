from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    username: str
    password: str